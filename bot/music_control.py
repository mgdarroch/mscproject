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
from bot.song_info import Songinfo


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




class MusicControl(object):
    #  The controller handles the playing of audio and the transition from one song to the next in the play queue.

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
    
    
    # getting the length of the playlis
    async def playlist_length(self):
        return len(self.playlist)
    
    # check if the bot is connected to the voice client
    async def is_connected(self):
        return self.voice_client.is_connected()
    
    # connect to the voice client (allow the bot to play music)
    async def register_voice_channel(self, channel):
        self.voice_client = await channel.connect()
            
    
    # stops the voice connection, this must be done before moving to a different channel
    async def stop_voice_connection(self):
        try:
            await self.stop_player()
            await self.voice_client.disconnect(force=True)
        except:
            pass
            

    # used to return a string of all songs played        
    def track_history(self):
        history_string = config.INFO_HISTORY_TITLE
        for trackname in self.playlist.trackname_history:
            history_string += "\n" + trackname
        return history_string
    
    # used to return a string of all songs in the queue
    def track_queue(self):
        queue_string = config.QUEUE_TITLE
        for trackname in self.playlist.playqueuename_history:
            queue_string += "\n" + trackname
        return queue_string


    # this is a coroutine loop which is run in a task to constantly play the next song in the playlist.
    # called when one song finishes playing, if there is no more songs the nickname of the bot is set to the default again.
    def next_song(self, error):
        
        self.current_songinfo = None
        next_song = self.playlist.next()

        if next_song is None:
            coro = self.guild.me.edit(nick=config.DEFAULT_NICKNAME)
        else:
            coro = self.play_youtube(next_song)

        self.client.loop.create_task(coro)
        
    # Reverts back to the previous song, initially you cuold get
    # caught in a loop by just spamming .prev but this has been fixed.
    async def prev_song(self):
        # gets the most recent song in the track history and plays it again
        if len(self.playlist.playhistory) == 0:
            return None
        if self.guild.voice_client is None or (
                not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            prev_song = self.playlist.prev()
            # Placeholder used if there is no song in the history.
            if prev_song == "Placeholder":
                self.playlist.next()
                return None
            await self.play_youtube(prev_song)
        else:
            self.playlist.prev()
            self.playlist.prev()
            self.guild.voice_client.stop()
        
        
        
        
        
    # asynchronous function to get the content of a site in text format.  Used here to access YouTube.
    async def get_site_content(self, url):
    
        headers= {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
        async with aiohttp.ClientSession(headers=headers) as session:
            print("URL BEING SEARCHED FOR: " + url)
            async with session.get(url) as resp:
                return await resp.text()


     # converts search terms to the YouTube link of the top video returned by the search.
    # this was a pain
    async def convert_to_youtube_link(self, title):
        filter(lambda x: x in set(printable), title)
        query = urllib.parse.quote(title)
        url = "https://www.youtube.com/results?search_query=" + query

        print(url)
        
        text = await self.get_site_content(url)
        text = ftfy.fix_encoding(text)

        # YOUTUBE CHANGED THINGS AGAIN AND NOW THIS WORKS
        text = text[text.find('{"responseContext":{"serviceTrackingParams":'):text.find('// scraper_data_end')]
        text = text[:-3]
        video_results = json.loads(text)

        # THIS USED TO BE THE WORKING VERSION
                
        # When this part of the project was done a few months ago now, Youtube search displayed with regular HTML.  It has since been changed
        # to display itself in JSON which is embedded inside a script tag so the page can be dynamically loaded.  This broke everything, forcing me
        # to use Selenium.  Selenium was too slow however and because it doesn't work well the async it caused blocking which then crashes the discord 
        # bot.  What follows is my attempt to rescue BeautifulSoup and keep this bot quick and efficient.  It works now, but Youtube may change something
        # again and completely break it in the future.

        

        #soup = BeautifulSoup(text, 'html5lib')
        #aid = soup.find('script',string=re.compile('ytInitialData'))

        #try:
        #    print("TRY")
        #    # This is a much neater way of doing things, but if the search turns up a video which has a ';' in it, this causes the JSON to be broken and have unterminated strings.
        #    script=aid.get_text().split(';')[0].replace('window["ytInitialData"] =','').strip()
        #    script = ftfy.fix_encoding(script)
        #    video_results=json.loads(script)
        #except ValueError:
        #    print("CATCH")
        #    # Because of the unterminated strings issue, I've had to do this, take off 108 characters from the end of the file.
        #    script=aid.get_text().replace('window["ytInitialData"] =','').strip()[:-15]
        #    script = ftfy.fix_encoding(script)
        #    video_results=json.loads(script)
        

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
    
    
    

    #  Intended for use in adding entire YouTube playlists.  Currently not working however.
    async def add_youtube(self, link):
        # Checks if a link is a playlist, if it is it parses the playlist, adding each video to the bot playlist
        # If link isn't a playlist this method is skipped over
        if not ("playlist?list=" in link):
            await self.add_song(link)
            return


        text = await self.get_site_content(link)
        soup = BeautifulSoup(text, 'html5lib')
        aid=soup.find('script',string=re.compile('ytInitialData'))
            
        # The following line is a much neater way of doing things, but if the search turns up a video which has a ';' in it, this causes the JSON to be broken and have unterminated strings.
        #script=aid.get_text().split(';')[0].replace('window["ytInitialData"] =','').strip()
        
        # Because of the unterminated strings issue, I've had to do this, take off 108 characters from the end of the file.
        script=aid.get_text().replace('window["ytInitialData"] =','').strip()[:-107]
        
        script = ftfy.fix_text(script)
        video_results=json.loads(script)
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


   

    # Adds a song to the bot's playlist.  If the song is the first one in the playlist the bot will begin playing the audio.
    
    async def add_song(self, track):
        # If the track is not a link, use the convert function to get the youtube link
        if not ("https://" in track):
            link = await self.convert_to_youtube_link(track)
            if link is None:
                link = await self.convert_to_youtube_link(track)
                if link is None:
                    return
        else:
            link = track
            
        
        # This is to get the title of the song to add it to the queue.  Initially this was not used 
        # and only the YouTube links were displayed in the queue, though after demand from users
        # this was changed.  Unfortunately, this slows down the process of play the music.  Could be removed if speed was a concern.
        try:
            extracted_info = youtube_dl.YoutubeDL({}).extract_info(link, download=False)
        except:
            print("Unable to download")
            
        self.playlist.add(link)
        self.playlist.add_name_queue(extracted_info.get('title'))
        if len(self.playlist.playqueue) == 1:
            await self.play_youtube(link)


    # This function handles the playing of the music.
    async def play_youtube(self, youtube_link):
        #Downloads and plays the audio of the youtube link passed
        # using FFmpeg

        try:
            downloader = youtube_dl.YoutubeDL({'format': 'bestaudio', 'title': True})
            extracted_info = downloader.extract_info(youtube_link, download=False)
        except:
            try:
                downloader = youtube_dl.YoutubeDL({})
                extracted_info = downloader.extract_info(youtube_link, download=False)
            except:
                self.next_song(None)

        
        # Update the songinfo
        self.current_songinfo = Songinfo(extracted_info.get('uploader'), extracted_info.get('creator'),
                                         extracted_info.get('title'), extracted_info.get('duration'),
                                         extracted_info.get('like_count'), extracted_info.get('dislike_count'),
                                         extracted_info.get('webpage_url'))

        # Bot nickname becomes what the songs title is
        await self.guild.me.edit(nick=playing_string(extracted_info.get('title')))
        self.playlist.add_name_history(extracted_info.get('title'))

        
        # Converts and streams the audio
        self.voice_client.play(discord.FFmpegPCMAudio(extracted_info['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'), after=lambda e: self.next_song(e))
        self.voice_client.source = discord.PCMVolumeTransformer(self.guild.voice_client.source)
        self.voice_client.source.volume = float(self.volume) / 100.0


    # Stops the bot transmitting audio and clears the playlist.
    async def stop_player(self):
        # stops the bot from transmitting audio in the voice channel
        if self.guild.voice_client is None or (
                not self.guild.voice_client.is_paused() and not self.guild.voice_client.is_playing()):
            return
        self.playlist.next()
        self.playlist.empty()
        self.guild.voice_client.stop()
        await self.guild.me.edit(nick=config.DEFAULT_NICKNAME)



