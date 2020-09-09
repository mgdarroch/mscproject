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
async def test_lyricsearch(interface):
    await interface.assert_reply_contains(".lyricsearch woke up I'm in the inbetween", "Results Found!")

@test_collector()
async def test_lyricplay(interface):
    await interface.assert_reply_contains(".lyricplay woke up I'm in the inbetween", "Added")
    
@test_collector()
async def test_songinfo(interface):
    await interface.assert_reply_contains(".songinfo", "Uploader:")

@test_collector()
async def test_pause(interface):
    await interface.assert_reply_contains(".pause", "Playback Paused")
    
@test_collector()
async def test_resume(interface):
    await interface.assert_reply_contains(".resume", "Resuming Playback")
    
@test_collector()
async def test_yt(interface):
    await interface.assert_reply_contains(".yt Bleachers Mickey Mantle", "Playing ")
    
@test_collector()
async def test_queue(interface):
    await interface.assert_reply_contains(".queue", "Song Queue:")
    
@test_collector()
async def test_skip(interface):
    await interface.assert_reply_contains(".skip", "Skipping song")


@test_collector()
async def test_history(interface):
    await interface.assert_reply_contains(".history", "Songs Played:")


@test_collector()
async def test_prev(interface):
    await interface.assert_reply_contains(".prev", "Playing previous song")


@test_collector()
async def test_stop(interface):
    await interface.assert_reply_contains(".stop", "Stopping all playback")
    
@test_collector()
async def test_vol(interface):
    await interface.assert_reply_contains(".vol 10", "Changing Volume")


@test_collector()
async def test_help(interface):
    await interface.assert_reply_contains(".help", "Type .help command for more info on a command.")
    
@test_collector()
async def test_spotify(interface):
    await interface.assert_reply_contains(".spotify", "Playing from Spotify")


@test_collector()
async def test_cc(interface):
    await interface.assert_reply_contains(".cc General", "Moving to channel:")


@test_collector()
async def test_disconnect(interface):
    await interface.assert_reply_contains(".disconnect", "Disconnected from channel")
    
@test_collector()
async def test_connect(interface):
    await interface.assert_reply_contains(".connect General", "Connected to ")

# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector, timeout=15)