from config import config

# A dictionary that remembers which guild belongs to which audiocontroller
guild_to_audiocontroller = {}


def get_guild(client, command):

    if command.guild is not None:
        return command.guild
    for guild in client.guilds:
        for channel in guild.voice_channels:
            if command.author in channel.members:
                return guild
    return None


async def send_message(ctx, message):
    await ctx.send("\n" + message + "\n")


async def connect_to_channel(guild, dest_channel_name, ctx, switch=False, default=True):

    for channel in guild.voice_channels:
        if str(channel.name).strip() == str(dest_channel_name).strip():
            if switch:
                try:
                    await guild.voice_client.disconnect()
                except:
                    await send_message(ctx, config.NOT_CONNECTED_MESSAGE)
            await channel.connect()
            return

    if default:
        try:
            await guild.voice_channels[0].connect()
        except:
            await send_message(ctx, config.DEFAULT_CHANNEL_JOIN_FAILED)
    else:
        await send_message(ctx, config.CHANNEL_NOT_FOUND_MESSAGE + str(dest_channel_name))
