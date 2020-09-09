from discord.ext import commands

from bot import utils
from bot import audiocontroller
from config import config


class Music(commands.Cog):
    """ A collection of the commands related to music playback.

        Attributes:
            bot: The instance of the bot that is executing the commands.
    """
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music Cog Loaded')


    @commands.command(name='yt', description = config.HELP_YT_LONG, help = config.HELP_YT_SHORT)
    async def _play_youtube(self, ctx, *, track: str):
        current_guild = utils.get_guild(self.client, ctx.message)

        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        audiocontroller = utils.guild_to_audiocontroller[current_guild]

        if track.isspace() or not track:
            return
        await audiocontroller.add_youtube(track)
        await utils.send_message(ctx, "Playing from Youtube...")

    @commands.command(name='pause', description= config.HELP_PAUSE_LONG, help = config.HELP_PAUSE_SHORT)
    async def _pause(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or not current_guild.voice_client.is_playing():
            return
        current_guild.voice_client.pause()
        await utils.send_message(ctx, "Playback Paused...")

    @commands.command(name='stop', description = config.HELP_STOP_LONG, help =config. HELP_STOP_SHORT)
    async def _stop(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].stop_player()
        await utils.send_message(ctx, "Stopping all playback...")

    @commands.command(name='skip', description = config.HELP_SKIP_LONG, help = config.HELP_SKIP_SHORT)
    async def _skip(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        if current_guild.voice_client is None or (
                not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            return
        current_guild.voice_client.stop()
        await utils.send_message(ctx, "Skipping song...")

    @commands.command(name='prev', description = config.HELP_PREV_LONG, help = config.HELP_PREV_SHORT)
    async def _prev(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        await utils.guild_to_audiocontroller[current_guild].prev_song()
        await utils.send_message(ctx, "Playing previous song...")

    @commands.command(name='resume', description = config.HELP_RESUME_LONG, help = config.HELP_RESUME_SHORT)
    async def _resume(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        current_guild.voice_client.resume()
        await utils.send_message(ctx, "Resuming Playback...")

    @commands.command(name='vol', aliases = ["volume"], description = config.HELP_VOL_LONG, help = config.HELP_VOL_SHORT)
    async def _volume(self, ctx, volume):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return

        utils.guild_to_audiocontroller[current_guild].volume = volume
        await utils.send_message(ctx, "Changing Volume...")

    @commands.command(name='spotify', description = config.HELP_SPOTIFY_LONG, help = config.HELP_SPOTIFY_SHORT)
    async def _spotify(self, ctx,  *, nick_name=None):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return

        spotify_member = None
        if not nick_name or nick_name.isspace():
            spotify_member = ctx.message.author

        else:
            for channel in current_guild.voice_channels:
                for member in channel.members:
                    if member.nick == nick_name or (member.nick is None and member.name == nick_name):
                        spotify_member = member

        if spotify_member is None:
            return
        if spotify_member.activity.name != "Spotify":
            return
        song = spotify_member.activity.title + " " + spotify_member.activity.artist

        await utils.guild_to_audiocontroller[current_guild].add_song(song)
        await utils.send_message(ctx, "Playing from Spotify...")

    @commands.command(name='songinfo', description = config.HELP_SONGINFO_LONG, help = config.HELP_SONGINFO_SHORT)
    async def _songinfo(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        songinfo = utils.guild_to_audiocontroller[current_guild].current_songinfo.output
        if songinfo is None:
            return
        await utils.send_message(ctx, songinfo)

    @commands.command(name='history', description = config.HELP_HISTORY_LONG, help = config.HELP_HISTORY_SHORT)
    async def _history(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        await utils.send_message(ctx,utils.guild_to_audiocontroller[current_guild].track_history())
        
        
    @commands.command(name='queue', description= config.HELP_QUEUE_LONG, help= config.HELP_HISTORY_SHORT)
    async def _queue(self, ctx):
        current_guild = utils.get_guild(self.client, ctx.message)
        if current_guild is None:
            await utils.send_message(ctx, config.NO_GUILD_MESSAGE)
            return
        await utils.send_message(ctx, utils.guild_to_audiocontroller[current_guild].track_queue())
        
    
def setup(client):
    client.add_cog(Music(client))
