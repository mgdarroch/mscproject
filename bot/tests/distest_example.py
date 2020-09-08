"""
A functional demo of all possible test cases. This is the format you will want to use with your testing bot.

    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
"""
import asyncio
import sys
from distest import TestCollector
from distest import run_interactive_bot, run_dtest_bot
from discord import Embed
import discord

# The tests themselves

test_collector = TestCollector()
created_channel = None

@test_collector()
async def test_chat(interface):
    await interface.assert_reply_contains(".chat Hello", "i m sorry , man . have you been ?")


@test_collector()
async def test_addbot(interface):
    await interface.assert_reply_contains(".addbot", "To add this bot to your own Server, click the following link:")


@test_collector()
async def test_cc(interface):
    await interface.assert_reaction_equals("React with \u2714 please!", u"\u2714")


@test_collector()
async def test_connect(interface):
    await interface.assert_reply_equals("Please say 'epic!'", "epic!")


@test_collector()
async def test_disconnect(interface):
    await interface.send_message("Create a tc called yeet")
    created_channel = await interface.assert_guild_channel_created("yeet")


# @test_collector
# async def test_pin_in_channel(interface):
#     await interface.send_message("Pin 'this is cool' in yeet")
#     await interface.assert_guild_channel_pin_content_equals(created_channel )


@test_collector()
async def test_lyricplay(interface):
    await interface.send_message("Delete that TC bro!")
    await interface.assert_guild_channel_deleted("yeet")


@test_collector()
async def test_lyricsearch(interface):
    await interface.send_message("Shhhhh...")
    await interface.ensure_silence()


@test_collector()
async def test_history(interface):
    await interface.assert_reply_contains(
        "Say something containing 'gamer' please!", "gamer"
    )


@test_collector()
async def test_pause(interface):
    await interface.assert_reply_matches(
        "Say something matching the regex `[0-9]{1,3}`", r"[0-9]{1,3}"
    )


@test_collector()
async def test_prev(interface):
    await interface.ask_human("Click the Check!")


@test_collector()
async def test_queue(interface):
    embed = (
        Embed(
            title="This is a test!",
            description="Descriptive",
            url="http://www.example.com",
            color=0x00FFCC,
        )
            .set_author(name="Author")
            .set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/4/40/Test_Example_%28cropped%29.jpg"
        )
            .set_image(
            url="https://upload.wikimedia.org/wikipedia/commons/4/40/Test_Example_%28cropped%29.jpg"
        )
    )

    # This image is in WikiMedia Public Domain
    await interface.assert_reply_embed_equals("Test the Embed!", embed)


@test_collector()
async def test_resume(interface):
    embed = Embed(title="Testing Title.", description="Wrong Description")
    await interface.assert_reply_embed_equals(
        "Test the Part Embed!", embed, attributes_to_check=["title"]
    )


@test_collector()
async def test_skip(interface):
    await interface.assert_reply_has_image("Post something with an image!")


@test_collector()
async def test_songinfo(interface):
    message = await interface.send_message("Say 'Yeah, that cool!'")
    await asyncio.sleep(1)
    await interface.edit_message(message, "Say 'Yeah, that is cool!'")
    await interface.assert_message_contains(message, "Yeah, that is cool!")


@test_collector()
async def test_spotify(interface):
    message = await interface.send_message("Say stuff in another channel")
    await asyncio.sleep(1)
    await interface.wait_for_message_in_channel("here is a message in another channel", 694397509958893640)
    
@test_collector()
async def test_stop(interface):
    message = await interface.send_message("Say stuff in another channel")
    await asyncio.sleep(1)
    await interface.wait_for_message_in_channel("here is a message in another channel", 694397509958893640)
    
@test_collector()
async def test_vol(interface):
    message = await interface.send_message("Say stuff in another channel")
    await asyncio.sleep(1)
    await interface.wait_for_message_in_channel("here is a message in another channel", 694397509958893640)

@test_collector()
async def test_yt(interface):
    message = await interface.send_message("Say stuff in another channel")
    await asyncio.sleep(1)
    await interface.wait_for_message_in_channel("here is a message in another channel", 694397509958893640)

@test_collector()
async def test_help(interface):
    message = await interface.send_message("Say stuff in another channel")
    await asyncio.sleep(1)
    await interface.wait_for_message_in_channel("here is a message in another channel", 694397509958893640)


# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)