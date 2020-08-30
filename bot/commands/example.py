import discord
from discord.ext import commands

class Example(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    #self must be the first parameter that every function in the class takes
    async def on_ready(self):
        print('Example Cog Loaded')
        
    
    #@commands.command()
    #async def ping(self, ctx):
        #await ctx.send('Pong! {}ms'.format(round(self.client.latency * 1000)))


def setup(client):
    client.add_cog(Example(client))