import urllib.request
import urllib.parse
import requests
from string import printable

import discord
import youtube_dl
from bs4 import BeautifulSoup

from config import config
from bot.playlist import Playlist
from bot.songinfo import Songinfo

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def playing_string(title):
    """Formats the name of the current song to better fit the nickname format."""
    filter(lambda x: x in set(printable), title)
    title_parts = title.split(" ")
    short_title = ""

    if len(title_parts) == 1:
        short_title = title[0:29]
    else:
        for part in title_parts:
            if len(short_title + part) > 28:
                break
            if short_title != "":
                short_title += " "
            short_title += part

    return "[" + short_title.replace("(", "|") + "]"


class AudioController(object):
    """ Controls the playback of audio and the sequential playing of the songs.

            Attributes:
                bot: The instance of the bot that will be playing the music.
                _volume: the volume of the music being played.
                playlist: A Playlist object that stores the history and queue of songs.
                current_songinfo: A Songinfo object that stores details of the current song.
                guild: The guild in which the Audiocontroller operates.
        """

    def __init__(self, client, guild, volume):
        self.client = client
        self._volume = volume
        self.playlist = Playlist()
        self.current_songinfo = None
        self.guild = guild
        self.voice_client = None

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        try:
            self.voice_client.source.volume = float(value) / 100.0
        except Exception as e:
            print(e)
        
    async def register_voice_channel(self, channel):
        self.voice_client = await channel.connect()
            
        

    def track_history(self):
        history_string = config.INFO_HISTORY_TITLE
        for trackname in self.playlist.trackname_history:
            history_string += "\n" + trackname
        return history_string
    
    def track_queue(self):
        queue_string = config.QUEUE_TITLE
        for trackname in self.playlist.playque:
            queue_string += "\n" + trackname
        return queue_string

    def next_song(self, error):
        """Invoked after a song is finished. Plays the next song if there is one, resets the nickname otherwise"""

        self.current_songinfo = None
        next_song = self.playlist.next()

        if next_song is None:
            coro = self.guild.me.edit(nick=config.DEFAULT_NICKNAME)
        else:
            coro = self.play_youtube(next_song)

        self.client.loop.create_task(coro)

    async def add_youtube(self, link):
        """Processes a youtube link and passes elements of a playlist to the add_song function one by one"""

        # Pass it on if it is not a playlist
        if not ("playlist?list=" in link):
            await self.add_song(link)
            return

        # Parse the playlist page html and get all the individual video links
        response = urllib.request.urlopen(link)
        print("Reading page")
        soup = BeautifulSoup(response.read(), "html.parser")
        res = soup.find_all('a', {'class': 'pl-video-title-link'})
        for l in res:
            await self.add_song('https://www.youtube.com' + l.get("href"))

    async def add_song(self, track):
        """Adds the track to the playlist instance and plays it, if it is the first song"""

        # If the track is a video title, get the corresponding video link first
        if not ("watch?v=" in track):
            link = self.convert_to_youtube_link(track)
        else:
            link = track
        self.playlist.add(link)
        if len(self.playlist.playque) == 1:
            await self.play_youtube(link)

    def convert_to_youtube_link(self, title):
        #Converts a query into a youtube link
        # Parse the search result page for the first results link
        search_words = title.split()
        search_url = "https://www.youtube.com/results?search_query=" + '+'.join(search_words)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())
        driver.get(search_url)
        continue_link = driver.find_element_by_tag_name('a')
        elems = driver.find_elements_by_xpath("//a[@href]")
        link = None
        for elem in elems:
            attribute = elem.get_attribute("href")
            if ("watch?v=") in attribute:
                link = attribute
                break
        driver.quit()
        return link


    async def play_youtube(self, youtube_link):
        """Downloads and plays the audio of the youtube link passed"""

        youtube_link = youtube_link.split("&list=")[0]

        try:
            downloader = youtube_dl.YoutubeDL({'format': 'bestaudio', 'title': True})
            extracted_info = downloader.extract_info(youtube_link, download=False)
        # "format" is not available for livestreams - redownload the page with no options
        except:
            try:
                downloader = youtube_dl.YoutubeDL({})
                extracted_info = downloader.extract_info(youtube_link, download=False)
            except:
                self.next_song(None)

        
        # Update the songinfo to reflect the current song
        self.current_songinfo = Songinfo(extracted_info.get('uploader'), extracted_info.get('creator'),
                                         extracted_info.get('title'), extracted_info.get('duration'),
                                         extracted_info.get('like_count'), extracted_info.get('dislike_count'),
                                         extracted_info.get('webpage_url'))

        # Change the nickname to indicate, what song is currently playing
        await self.guild.me.edit(nick=playing_string(extracted_info.get('title')))
        self.playlist.add_name(extracted_info.get('title'))
        
        self.voice_client.play(discord.FFmpegPCMAudio(extracted_info['url']), after=lambda e: self.next_song(e))
        self.voice_client.source = discord.PCMVolumeTransformer(self.guild.voice_client.source)
        self.voice_client.source.volume = float(self.volume) / 100.0

    async def stop_player(self):
        """Stops the player and removes all songs from the queue"""
        if self.guild.voice_client is None or (
                not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            return
        self.playlist.next()
        self.playlist.playque.clear()
        self.guild.voice_client.stop()
        await self.guild.me.edit(nick=config.DEFAULT_NICKNAME)

    async def prev_song(self):
        """Loads the last ong from the history into the queue and starts it"""
        if len(self.playlist.playhistory) == 0:
            return None
        if self.guild.voice_client is None or (
                not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            prev_song = self.playlist.prev()
            # The Dummy is used if there is no song in the history
            if prev_song == "Dummy":
                self.playlist.next()
                return None
            await self.play_youtube(prev_song)
        else:
            self.playlist.prev()
            self.playlist.prev()
            self.guild.voice_client.stop()
