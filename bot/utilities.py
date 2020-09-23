from config import config

# A dictionary that remembers which guild belongs to which MusicControl
guild_to_musiccontrol = {}


def get_guild(client, command):

    if command.guild is not None:
        return command.guild
    for guild in client.guilds:
        for channel in guild.voice_channels:
            if command.author in channel.members:
                return guild
    return None


async def get_channel(guild, channel_name):
    for channel in guild.voice_channels:
        if str(channel.name).strip() == str(channel_name).strip():
            return channel
    return None
        

async def send_message(ctx, message):
    await ctx.send("\n" + message + "\n")