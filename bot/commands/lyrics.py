import lyricsgenius
import discord
from discord.ext import commands
import sys  
import re
import aiohttp
import asyncio
import urllib.parse
import json
import codecs
import os
import socket
import collections
import ftfy
import html5lib
from socket import AF_INET, SOCK_DGRAM
from bot import audiocontroller
from bot import utils
from config import config
from bot import songinfo
from bs4 import BeautifulSoup, UnicodeDammit

def load_credentials():
    client_id = config.CLIENT_ID
    client_secret = config.CLIENT_SECRET
    client_access_token = config.CLIENT_ACCESS_TOKEN
    return client_id, client_secret, client_access_token

async def get_site_content_as_json(url, auth_token):
    headers= {"Authorization": "Bearer Guxci2VxlB5aOZ5O5RXUARnBBkfyNcyiE02UI_kGQz-H2Am1me6q72bYXHlJZ4ue"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            return await resp.json()
    
async def get_site_content(url, auth_token):
    cookies = {'cookies_are': 'working'}
    headers={"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, cookies) as resp:
            return await resp.text()
    
async def search(search_term,client_access_token):
    return_list = []
    page=1
    print("TITLE BEING SEARCHED FOR: " + search_term)
    while page < 2:
        auth_token = client_access_token
        querystring = "https://api.genius.com/search?q=" + urllib.parse.quote(search_term) + "&page=" + str(page)
        print("QUERYSTRING: " + querystring)
        json_data = await get_site_content_as_json(querystring, auth_token)
        json_str = json.dumps(json_data)
        json_str = ftfy.fix_encoding(json_str)
        json_data = json.loads(json_str)
        body = json_data["response"]["hits"]
        #with open("geniusjson.json", "w+") as f:
        #    f.write(json.dumps(body))

        num_hits = len(body)
        if num_hits==0:
            if page==1:
                print("No results for: " + search_term)
            break      
        print("page {0}; num hits {1}".format(page, num_hits))
            
        for result in body:
            result_id = result["result"]["id"]
            title = result["result"]["title"].replace("’", "'")
            url = result["result"]["url"]
            path = result["result"]["path"]
            primaryartist_id = result["result"]["primary_artist"]["id"]
            primaryartist_name = result["result"]["primary_artist"]["name"].replace("’", "'").replace("m", "m")
            row=[result_id,title,url,path,primaryartist_id,primaryartist_name]
            return_list.append(row)
        print("{0} results found".format(num_hits))
        page+=1
    return return_list

#async def get_lyrics(url, client_access_token):
#    site_content = await get_site_content(url, client_access_token)
#    with open("lyrics_site.txt", "w+") as f:
#        f.write(site_content)
#    soup = BeautifulSoup(site_content, 'html5lib')
#    lyrics_site = soup.find("div", class_="lyrics")
#    lyrics = UnicodeDammit(lyrics_site.get_text().strip()).unicode_markup
#    
#    return lyrics
    
            

class Lyrics(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.client_id = None
        self.client_secret = None
        self.client_access_token = None
        
        
    @commands.Cog.listener()
    #self must be the first parameter that every function in the class takes
    async def on_ready(self):
        self.client_id, self.client_secret, self.client_access_token = load_credentials()
        genius = lyricsgenius.Genius(self.client_access_token)
        print('Lyrics Cog Loaded')
        
    @commands.command(description=config.HELP_LYRICSEARCH_LONG, help=config.HELP_LYRICSEARCH_SHORT)
    async def lyricsearch(self, ctx, *, lyrics):
        results = await search(lyrics, self.client_access_token)
        await utils.send_message(ctx, "Results Found!")
        message = ''
        line_count = 1
        
        for song in results:
            message += "{0}. {1} - {2}\n".format(line_count,song[1], song[5])
            line_count += 1
        await utils.send_message(ctx, message)
        
    
    @commands.command(description = config.HELP_LYRICPLAY_LONG, help = config.HELP_LYRICPLAY_SHORT)
    async def lyricplay(self, ctx, *, lyrics):
        results = await search(lyrics, self.client_access_token)
        search_term = ""
        
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        
        for song in results:
            search_term += "{} {}".format(song[1], song[5])
            break
            
        await audiocontroller.add_song(search_term)
        await utils.send_message(ctx, "Added {} to playlist...".format(song[1]))
        
    #@commands.command(description= config.HELP_GETLYRICS_LONG, help= config.HELP_GETLYRICS_SHORT)
    #async def getlyrics(self, ctx, *, lyrics):
    #    print("TITLE BEING SEARCHED FOR: " + lyrics)
    #    client_id, client_secret, client_access_token = load_credentials()
    #    results = await search(lyrics, client_access_token)
    #    path = ""
    #    for song in results:
    #        path = "https://genius.com/{}".format(song[3])
    #        break
    #    print(path)
    #    lyrics = await get_lyrics(path, client_access_token)
    #    utils.send_message(ctx, lyrics)
        

def setup(client):
    client.add_cog(Lyrics(client))
