import lyricsgenius
import discord
from discord.ext import commands
import sys  
import re
import urllib.request
import urllib.parse
import json
import csv
import codecs
import os
import socket
import collections
from socket import AF_INET, SOCK_DGRAM
from bot import audiocontroller
from bot import utils
import config

def load_credentials():
    lines = [line.rstrip('\n') for line in open('bot/commands/credentials.ini')]
    chars_to_strip = " \'\""
    for line in lines:
        if "client_id" in line:
            client_id = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        if "client_secret" in line:
            client_secret = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
        #Currently only need access token to run, the other two perhaps for future implementation
        if "client_access_token" in line:
            client_access_token = re.findall(r'[\"\']([^\"\']*)[\"\']', line)[0]
    return client_id, client_secret, client_access_token

    
def search(search_term,client_access_token):
    return_list = []
    page=1
    while page < 2:
        querystring = "http://api.genius.com/search?q=" + urllib.parse.quote(search_term) + "&page=" + str(page)
        request_att = urllib.request.Request(querystring)
        request_att.add_header("Authorization", "Bearer " + client_access_token)   
        request_att.add_header("User-Agent", "curl/7.9.8 (i686-pc-linux-gnu) libcurl 7.9.8 (OpenSSL 0.9.6b) (ipv6 enabled)") #Must include user agent of some sort, otherwise 403 returned
        while True:
            try:
                response = urllib.request.urlopen(request_att, timeout=4) #timeout set to 4 seconds; automatically retries if times out
                raw = response.read()
            except socket.timeout:
                print("Timeout raised and caught")
                continue
            break
        json_obj = json.loads(raw)
        body = json_obj["response"]["hits"]

        num_hits = len(body)
        if num_hits==0:
            if page==1:
                print("No results for: " + search_term)
            break      
        print("page {0}; num hits {1}".format(page, num_hits))
            
        for result in body:
            result_id = result["result"]["id"]
            title = result["result"]["title"].replace("’", "'").replace("m", "m")
            url = result["result"]["url"]
            path = result["result"]["path"]
            primaryartist_id = result["result"]["primary_artist"]["id"]
            primaryartist_name = result["result"]["primary_artist"]["name"].replace("’", "'").replace("m", "m")
            row=[result_id,title,url,path,primaryartist_id,primaryartist_name]
            return_list.append(row)
        print("{0} results found".format(num_hits))
        page+=1
    return return_list
            

class Lyrics(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    #self must be the first parameter that every function in the class takes
    async def on_ready(self):
        genius = lyricsgenius.Genius("71Qqk2gCXUJWt1hBCqIdl4cXXSkpqchoGygISzHMKVNv0fn2E_hHouppZp6Ft1iD")
        print('Lyrics Cog Loaded')
        
    @commands.command()
    async def lyricsearch(self, ctx, *, lyrics):
        client_id, client_secret, client_access_token = load_credentials()
        results = search(lyrics, client_access_token)
        await ctx.send("Results Found!")
        message = ''
        line_count = 1
        
        for song in results:
            message += "{0}. {1} - {2}\n".format(line_count,song[1], song[5])
            line_count += 1
        await ctx.send(message)
        
    
    @commands.command()
    async def lyricplay(self, ctx, *, lyrics):
        client_id, client_secret, client_access_token = load_credentials()
        results = search(lyrics, client_access_token)
        search_term = ""
        
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        audiocontroller = utils.guild_to_audiocontroller[current_guild]
        
        for song in results:
            search_term += "{} {}".format(song[1], song[5])
            break
            
        track = audiocontroller.convert_to_youtube_link(search_term)
        await audiocontroller.add_youtube(track)
        

def setup(client):
    client.add_cog(Lyrics(client))
