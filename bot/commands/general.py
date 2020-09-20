from discord.ext import commands

from config import config
from bot import utils
from bot.audiocontroller import AudioController


class General(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('General Cog Loaded')
        
    
    @commands.command(name='summon', description=config.HELP_SUMMON_LONG, help=config.HELP_SUMMON_SHORT)
    async def _summon(self, ctx):
        current_guild = ctx.message.guild
        dest_channel_name = ctx.message.author.voice.channel
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        
        if utils.guild_to_audiocontroller[current_guild] is None:
            utils.guild_to_audiocontroller[current_guild] = AudioController(self.client, current_guild, config.DEFAULT_VOLUME)
            
        if await utils.guild_to_audiocontroller[current_guild].is_connected():
            await utils.guild_to_audiocontroller[current_guild].stop_voice_connection()
            
        await utils.guild_to_audiocontroller[current_guild].register_voice_channel(await utils.get_channel(current_guild, dest_channel_name))
        
        if await utils.guild_to_audiocontroller[current_guild].is_connected():
            print("CLIENT CONNECTED TO VOICE")
        
        msg = "Connected to " + dest_channel_name
        await utils.send_message(ctx, msg)
        ## Automatically finds the command sender's channel and connects to it
        

    @commands.command(name='connect', description=config.HELP_CONNECT_LONG, help=config.HELP_CONNECT_SHORT)
    async def _connect(self, ctx, *, dest_channel_name: str):
        current_guild = ctx.message.guild

        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return

        if utils.guild_to_audiocontroller[current_guild] is None:
            utils.guild_to_audiocontroller[current_guild] = AudioController(self.client, current_guild, config.DEFAULT_VOLUME)
            
        if await utils.guild_to_audiocontroller[current_guild].is_connected():
            await utils.guild_to_audiocontroller[current_guild].stop_voice_connection()
        
        await utils.guild_to_audiocontroller[current_guild].register_voice_channel(await utils.get_channel(current_guild, dest_channel_name))
        
        if await utils.guild_to_audiocontroller[current_guild].is_connected():
            print("CLIENT CONNECTED TO VOICE")
        
        msg = "Connected to " + dest_channel_name
        await utils.send_message(ctx, msg)


    @commands.command(name='disconnect', description=config.HELP_DISCONNECT_LONG, help=config.HELP_DISCONNECT_SHORT)
    async def _disconnect(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)

        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        
        await utils.guild_to_audiocontroller[current_guild].stop_voice_connection()
        await utils.send_message(ctx, "Disconnected from channel")
        

    @commands.command(name='cc', aliases=["changechannel"], description=config.HELP_CC_LONG, help=config.HELP_CC_SHORT)
    async def _changechannel(self, ctx, *, dest_channel_name: str):
        current_guild = utils.get_guild(self.client, ctx.message)

        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        
        await utils.guild_to_audiocontroller[current_guild].stop_voice_connection()
        await utils.guild_to_audiocontroller[current_guild].register_voice_channel(await utils.get_channel(current_guild, dest_channel_name))
        if await utils.guild_to_audiocontroller[current_guild].is_connected():
            print("CLIENT CONNECTED TO VOICE")
        msg = "Moving to channel: " + dest_channel_name
        await utils.send_message(ctx, msg)


    @commands.command(name='addbot', description=config.HELP_ADDBOT_LONG, help=config.HELP_ADDBOT_SHORT)
    async def _addbot(self, ctx):
        await ctx.send(config.ADD_MESSAGE_1 + str(self.client.user.id) + config.ADD_MESSAGE_2)


def setup(client):
    client.add_cog(General(client))
