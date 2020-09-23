import discord
from discord.ext import commands

# BASIC ADMINISTRATIVE TOOLS.  NOT NECESSARY MOST SERVERS HAVE BETTER ONES.

class AdminTools(commands.Cog):
    
    def __init__(self, client):
        self.client = client 
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('AdminTools Cog Loaded')
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong! {}ms'.format(round(self.client.latency * 1000)))
        
    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
    

# Kick, ban functionality
    
    @commands.command()
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
    
    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
    
    @commands.command()
    async def unban(self, ctx, member : discord.Member, *, reason=None):
        await member.unban(reason=reason)

def setup(client):
    client.add_cog(AdminTools(client))