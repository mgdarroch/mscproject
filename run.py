import discord
from discord.ext import commands

from config.config import *
from bot.audiocontroller import AudioController
from bot.utils import guild_to_audiocontroller


initial_extensions = ['bot.commands.music', 'bot.commands.general', 'bot.commands.chatbot', 'bot.commands.lyrics']
client = commands.Bot(command_prefix=".", pm_help=True)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            print(e)


@client.event
async def on_ready():
    print(STARTUP_MESSAGE)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=" Music, type .help "))

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


client.run(token, bot=True, reconnect=True)
