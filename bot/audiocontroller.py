# Imports for discord and Selenium for parsing web pages
import discord
import youtube_dl
import urllib.parse
import urllib.request
import requests
import urllib.request
import asyncio
import aiohttp
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from string import printable


from arsenic import get_session, keys, browsers, services

# imports for AudioController object
from config import config
from bot.playlist import Playlist
from bot.songinfo import Songinfo






def playing_string(title):
    # string reformatting for displaying the song title on the discord bot name
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
    #  The audiocontroller handles the playing of audio and the transition from one song to the next in the play queue.

    def __init__(self, client, guild, volume):
        # initialisation values
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
        for trackname in self.playlist.playqueue:
            queue_string += "\n" + trackname
        return queue_string

    def next_song(self, error):
        # called when one song finishes playing, if there is no more songs the nickname of the bot is set to the default again.

        self.current_songinfo = None
        next_song = self.playlist.next()

        if next_song is None:
            coro = self.guild.me.edit(nick=config.DEFAULT_NICKNAME)
        else:
            coro = self.play_youtube(next_song)

        self.client.loop.create_task(coro)

    async def add_youtube(self, link):
        
        service = services.Geckodriver(binary=config.GECKODRIVER)
        browser = browsers.Firefox()
        async with get_session(service, browser) as session:
            await session.get(link)
            elems = await session.wait_for_element()
        # Checks if a link is a playlist, if it is it parses the playlist, adding each video to the bot playlist

        # If link isn't a playlist this method is skipped over
        if not ("playlist?list=" in link):
            await self.add_song(link)
            return

        # Parse the playlist page html and get all the individual video links
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())
        driver.get(link)
        continue_link = driver.find_element_by_tag_name('a')
        elems = driver.find_elements_by_xpath("//a[@href]")
        link = ""
        for elem in elems:
            attribute = elem.get_attribute("href")
            if ("watch?v=") in attribute:
                link = attribute
                await self.add_song(link)
        driver.quit()


            
    async def add_song(self, track):
        # Adds a song to the bot's playlist.  If the song is the first one in the playlist the bot will begin playing the audio.

        # If the track is a video title, get the youtube link
        if not ("watch?v=" in track):
            link = self.convert_to_youtube_link(track)
        else:
            link = track
        self.playlist.add(link)
        if len(self.playlist.playqueue) == 1:
            await self.play_youtube(link)

    def convert_to_youtube_link(self, title):
        # takes a string and converts it to a query on youtube
        # the resulting search is then parsed and the first link is selected.  Not 100% accurate and you won't always get the video you want.
        search_words = title.split()
        search_url = "https://www.youtube.com/results?search_query=" + '+'.join(search_words)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        #driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
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
        #  Gets the info of the video
        # Then streams the video audio and plays it in the voice channel

        youtube_link = youtube_link.split("&list=")[0]

        try:
            downloader = youtube_dl.YoutubeDL({'format': 'bestaudio', 'title': True})
            extracted_info = downloader.extract_info(youtube_link, download=False)
        except:
            try:
                downloader = youtube_dl.YoutubeDL({})
                extracted_info = downloader.extract_info(youtube_link, download=False)
            except:
                self.next_song(None)

        
        # updates song info
        self.current_songinfo = Songinfo(extracted_info.get('uploader'), extracted_info.get('creator'),
                                         extracted_info.get('title'), extracted_info.get('duration'),
                                         extracted_info.get('like_count'), extracted_info.get('dislike_count'),
                                         extracted_info.get('webpage_url'))

        # the nickname of the bot is changed to the title of the video
        await self.guild.me.edit(nick=playing_string(extracted_info.get('title')))
        self.playlist.add_name(extracted_info.get('title'))
        
        self.voice_client.play(discord.FFmpegPCMAudio(extracted_info['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'), after=lambda e: self.next_song(e))
        self.voice_client.source = discord.PCMVolumeTransformer(self.guild.voice_client.source)
        self.voice_client.source.volume = float(self.volume) / 100.0

    async def stop_player(self):
        # stops the bot from transmitting audio in the voice channel
        if self.guild.voice_client is None or (
                not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            return
        self.playlist.next()
        self.playlist.playqueue.clear()
        self.guild.voice_client.stop()
        await self.guild.me.edit(nick=config.DEFAULT_NICKNAME)

  
  
    async def prev_song(self):
        # gets the most recent song in the track history and plays it again
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
