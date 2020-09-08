import pytest
from bot.audiocontroller import AudioController
import bot.audiocontroller
import bot.playlist
from bot.utils import guild_to_audiocontroller
from config import config
import discord
from discord.ext import commands
from bot.playlist import Playlist


def test_track_history():
    client = commands.Bot(command_prefix=".", pm_help=True)
    guild = None
    test_controller = AudioController(client, guild, config.DEFAULT_VOLUME)
    link1 = "https://youtu.be/bvFHRNGYfuo"
    link2 = "https://youtu.be/eclbaC3q94k"
    test_controller.playlist.add("https://youtu.be/bvFHRNGYfuo")
    test_controller.playlist.add("https://youtu.be/eclbaC3q94k")
    test_controller.playlist.next()
    test_controller.playlist.next()
    return_string = test_controller.track_history()
    assert link1, link2 in return_string


def test_track_queue():
    client = commands.Bot(command_prefix=".", pm_help=True)
    guild = None
    test_controller = AudioController(client, guild, config.DEFAULT_VOLUME)
    link1 = "https://youtu.be/bvFHRNGYfuo"
    link2 = "https://youtu.be/eclbaC3q94k"
    test_controller.playlist.add("https://youtu.be/bvFHRNGYfuo")
    test_controller.playlist.add("https://youtu.be/eclbaC3q94k")
    return_string = test_controller.track_queue()
    assert link1, link2 in return_string

def test_next_song():
    client = commands.Bot(command_prefix=".", pm_help=True)
    guild = None
    test_controller = AudioController(client, guild, config.DEFAULT_VOLUME)
    link1 = "https://youtu.be/bvFHRNGYfuo"
    link2 = "https://youtu.be/eclbaC3q94k"
    test_controller.playlist.add(link1)
    test_controller.playlist.add(link2)
    test_controller.playlist.next()
    return_string1 = test_controller.track_queue()
    return_string2 = test_controller.track_history()
    assert link2 in return_string1 and link1, link2 in return_string2

def test_convert_to_youtube_link():
    client = commands.Bot(command_prefix=".", pm_help=True)
    guild = None
    test_controller = AudioController(client, guild, config.DEFAULT_VOLUME)
    search_term = "hear all the bombs fade away"
    link = test_controller.convert_to_youtube_link(search_term)
    assert link == "https://www.youtube.com/watch?v=E5H8DwJI0uA"
    
    
def test_add_youtube():
    pass
    
def test_add_song():
    pass
    
def test_prev_song():
    pass