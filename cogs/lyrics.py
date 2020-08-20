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
from socket import AF_INET, SOCK_DGRAM

def load_credentials():
    lines = [line.rstrip('\n') for line in open('cogs/credentials.ini')]
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

def filesetup(search_term):
    if not os.path.exists("output/"):
        os.makedirs("output/")    
    outputfilename = "output/output-" + re.sub(r"[^A-Za-z]+", '', search_term) + ".csv"
    with codecs.open(outputfilename, 'ab', encoding='utf8') as outputfile:
        outwriter = csv.writer(outputfile)
        if os.stat(outputfilename).st_size == 0:
            header = ["id","title","url","path","primaryartist_id","primaryartist_name"]
            outwriter.writerow(header)
            return outputfilename
        else:
            return outputfilename
    
def search(search_term,outputfilename,client_access_token):
    with codecs.open(outputfilename, 'ab', encoding='utf8') as outputfile:
        outwriter = csv.writer(outputfile)
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
                title = result["result"]["title"].replace("’", "'")
                url = result["result"]["url"]
                path = result["result"]["path"]
                #header_image_url = result["result"]["header_image_url"]
                #annotation_count = result["result"]["annotation_count"]
                #pyongs_count = result["result"]["pyongs_count"]
                primaryartist_id = result["result"]["primary_artist"]["id"]
                primaryartist_name = result["result"]["primary_artist"]["name"].replace("’", "'")
                #primaryartist_url = result["result"]["primary_artist"]["url"]
                #primaryartist_imageurl = result["result"]["primary_artist"]["image_url"]
                row=[result_id,title,url,path,primaryartist_id,primaryartist_name]
                outwriter.writerow(row) #write as CSV
            print("{0} results found".format(num_hits))
            page+=1
            

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
        outputfilename = filesetup(lyrics)
        client_id, client_secret, client_access_token = load_credentials()
        search(lyrics, outputfilename, client_access_token)
        await ctx.send("Results Found!")
        message = ''
        with open(outputfilename, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 1
            for row in csv_reader:
                if row[0] == 'id':
                    continue
                message += "{0}. {1} - {2}\n".format(line_count,row[1], row[5])
                line_count+= 1
        await ctx.send(message)

def setup(client):
    client.add_cog(Lyrics(client))
