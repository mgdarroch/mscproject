import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
        print('Bot ready.')
    
@client.event
async def on_member_join(member):
    print('{} has joined the server'.format(member))
    
@client.event
async def on_member_remove(member):
    print('{} has left the server'.format(member))


@client.command()
# searches for a movie quote on IMDB? Maybe don't implement.
async def quote(ctx):
    pass

@client.command()
# will play the audio of a youtube video in the voice channel of the user who typed the command
async def play(ctx):
    pass


# COGS

@client.command()
async def load(ctx, extension):
    client.load_extension('commands.{}'.format(extension))
    print('{} has been loaded.'.format(extension))
    await ctx.send('{} has been loaded.'.format(extension))
    
@client.command()
async def unload(ctx, extension):
    client.unload_extension('cogs.{}'.format(extension))
    print('{} has been unloaded.'.format(extension))
    await ctx.send('{} has been unloaded.'.format(extension))
    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension('cogs.{}'.format(filename[:-3]))
        
        


# connect the chatbot.
# create a function in the chatbot program to take in one question and give a response,
# then return that response as a message in the discord channel.
# implement a way to deal with spam
# keep track of which servers the bot is connected to
# keep track of which users are connected to the server
# keep track of which channels each user is connected to? Maybe.

client.run('NzMzMzQ4MDg0NzEyNzM0NzIw.XxB7Eg.dLye5X1qpWkmTbvqThJ2n8Kp6_E')