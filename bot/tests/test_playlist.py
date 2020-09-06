import pytest
from bot.playlist import Playlist
import bot.playlist

def test_add_name():
    playlist = Playlist()
    # add Track 1 to the trackname_history
    playlist.add_name("Track 1")
    assert len(playlist.trackname_history) == 1
    

def test_add():
    playlist = Playlist()
    playlist.add("https://youtu.be/bvFHRNGYfuo")
    assert len(playlist.playque) == 1

def test_next():
    playlist = Playlist()
    # add two tracks to the playque
    playlist.add("https://youtu.be/bvFHRNGYfuo")
    playlist.add("https://youtu.be/eclbaC3q94k")
    # skip one, which should add the first track to the playhistory and pop it off the playque
    playlist.next()
    # leaving 1 track in the playque and 1 track in the playhistory
    assert len(playlist.playque) == 1 & len(playlist.playhistory) == 1

def test_prev():
    playlist = Playlist()
    playlist.add("https://youtu.be/eclbaC3q94k")
    # removes the track from the playque
    playlist.next()
    # should place the track just removed back into the playque
    playlist.prev()
    # leaving one track in the playque
    assert len(playlist.playque) == 1 

def test_empty():
    playlist = Playlist()
    # adds two songs to the playque
    playlist.add("https://youtu.be/bvFHRNGYfuo")
    playlist.add("https://youtu.be/eclbaC3q94k")
    # empties the playque
    playlist.empty()
    # leaving no songs in the playque
    assert len(playlist.playque) == 0