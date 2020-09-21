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
async def test_lyricplay(interface):
    await interface.assert_reply_contains(".lyricplay woke up I'm in the inbetween", "Added")
    
@test_collector()
async def test_lyricplay(interface):
    await interface.assert_reply_contains(".lyricplay heard from your mother she don't recognise you", "Added")
    
@test_collector()
async def test_lyricplay(interface):
    await interface.assert_reply_contains(".lyricplay i'll be coming into focus ill be waiting into focus", "Added")
    
@test_collector()
async def test_lyricplay(interface):
    await interface.assert_reply_contains(".lyricplay they closed the parkway late last night", "Added")
    
@test_collector()
async def test_lyricplay(interface):
    await interface.assert_reply_contains(".lyricplay such a rollercoaster some killer queen you are", "Added")
    
@test_collector()
async def test_lyricplay(interface):
    await interface.assert_reply_contains(".lyricplay a shimmering balance act I think that I laughed at that", "Added")
    
    
@test_collector()
async def test_play(interface):
    await interface.assert_reply_contains(".play Bleachers Goodmorning", "song to the playlist ")
    
@test_collector()
async def test_play(interface):
    await interface.assert_reply_contains(".play Bleachers Mickey Mantle", "song to the playlist ")
    
@test_collector()
async def test_play(interface):
    await interface.assert_reply_contains(".play Bleachers All My Heroes", "song to the playlist ")
    
@test_collector()
async def test_play(interface):
    await interface.assert_reply_contains(".play Bleachers Wild Heart", "song to the playlist ")
    
@test_collector()
async def test_play(interface):
    await interface.assert_reply_contains(".play Bleachers Rollercoaster", "song to the playlist ")
    
@test_collector()
async def test_play(interface):
    await interface.assert_reply_contains(".play Bleachers Don't Take The Money", "song to the playlist ")
    

# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)