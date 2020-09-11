import discord
import os
from discord.ext import commands
from config.config import *
from bot.audiocontroller import AudioController
from bot.utils import guild_to_audiocontroller

class TestableBot(commands.Bot):
    def __init__(self, command_prefix=".", **options):
        super().__init__(command_prefix, **options)
        
    async def process_commands(self, message):
        ctx = await self.get_context(message)
        await self.invoke(ctx)

# 'bot.commands.chatbot'
initial_extensions = ['bot.commands.music', 'bot.commands.general', 'bot.commands.lyrics']
client = TestableBot(command_prefix=".", pm_help=True)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(e)
            

@client.event
async def on_ready():
    print(STARTUP_MESSAGE)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=" Music, type .help"))

    for guild in client.guilds:
        print(guild.name)
        await guild.me.edit(nick=DEFAULT_NICKNAME)
        guild_to_audiocontroller[guild] = AudioController(client, guild, DEFAULT_VOLUME)
        try:
            await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
        except:
            print("could not join "+guild.name)
        
    print(STARTUP_COMPLETE_MESSAGE)


@client.event
async def on_guild_join(guild):
    print(guild.name)
    guild_to_audiocontroller[guild] = AudioController(client, guild, DEFAULT_VOLUME)
    try:
        await guild_to_audiocontroller[guild].register_voice_channel(guild.voice_channels[0])
    except:
        print("could not join "+guild.name)
    

@client.command()
async def load(ctx, extension):
    client.load_extension('commands.{}'.format(extension))
    print('{} has been loaded.'.format(extension))
    await ctx.send('{} has been loaded.'.format(extension))
    
@client.command()
async def unload(ctx, extension):
    client.unload_extension('commands.{}'.format(extension))
    print('{} has been unloaded.'.format(extension))
    await ctx.send('{} has been unloaded.'.format(extension))
        
    
    
client.run(token, bot=True, reconnect=True)
