# Imports for discord and Selenium for parsing web pages
import discord
import youtube_dl
import urllib.parse
import urllib.request
import urllib.request
import asyncio
import aiohttp
import sys
import html5lib
import ftfy
import re
import json
from string import printable
from bs4 import BeautifulSoup

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
        
        
    async def get_site_content(self, url):
        headers= {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            print("URL BEING SEARCHED FOR: " + url)
            async with session.get(url) as resp:
                return await resp.text()

    async def add_youtube(self, link):
        # Checks if a link is a playlist, if it is it parses the playlist, adding each video to the bot playlist
        # If link isn't a playlist this method is skipped over
        if not ("playlist?list=" in link):
            await self.add_song(link)
            return


        text = await self.get_site_content(link)
        soup = BeautifulSoup(text, 'html5lib')
        aid=soup.find('script',string=re.compile('ytInitialData'))
        script=aid.get_text().split(';')[0].replace('window["ytInitialData"] =','').strip()
        script = ftfy.fix_text(script)
        video_results=json.loads(script)
        json_out = json.dump(video_results, open("script.json", "w", encoding="utf-8"))
        item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        links = []
        for item in item_section:
            try:
                video_info=item["videoRenderer"]
                url=video_info["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
                link = "https://www.youtube.com" + url
                links.append(link)
            except KeyError:
                pass
        
        for link in links:
            self.add_song(link)


    async def convert_to_youtube_link(self, title):
        filter(lambda x: x in set(printable), title)
        query = urllib.parse.quote(title)
        url = "https://www.youtube.com/results?search_query=" + query
        
        text = await self.get_site_content(url)
        soup = BeautifulSoup(text, 'html5lib')
        aid=soup.find('script',string=re.compile('ytInitialData'))
        script=aid.get_text().split(';')[0].replace('window["ytInitialData"] =','').strip()
        script = ftfy.fix_text(script)
        video_results=json.loads(script)
        json_out = json.dump(video_results, open("script.json", "w", encoding="utf-8"))
        item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        
        urls = []
        for item in item_section:
            try:
                video_info=item["videoRenderer"]
                url=video_info["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
                urls.append(url)
            except KeyError:
                pass
            
        link = "https://www.youtube.com" + urls[0]
        return link

       
            
    async def add_song(self, track):
        # Adds a song to the bot's playlist.  If the song is the first one in the playlist the bot will begin playing the audio.
        # If the track is a video title, get the youtube link
        if not ("https://" in track):
            link = await self.convert_to_youtube_link(track)
            if link is None:
                link = await self.convert_to_youtube_link(track)
                if link is None:
                    return
        else:
            link = track
        self.playlist.add(link)
        if len(self.playlist.playqueue) == 1:
            await self.play_youtube(link)
            

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
        
        self.voice_client.play(discord.FFmpegPCMAudio(extracted_info['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'), after=lambda e: self.next_song(e))
        self.voice_client.source = discord.PCMVolumeTransformer(self.guild.voice_client.source)
        self.voice_client.source.volume = float(self.volume) / 100.0

    async def stop_player(self):
        # stops the bot from transmitting audio in the voice channel
        if self.guild.voice_client is None or (
                not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            return
        self.playlist.next()
        self.playlist.empty()
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
