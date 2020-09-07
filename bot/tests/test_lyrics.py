import pytest
import bot.commands.lyrics as lyrics
from config import config


def test_load_credentials():
    client_id, client_secret, client_access_token = lyrics.load_credentials()
    test_client_id = config.CLIENT_ID
    test_client_secret = config.CLIENT_SECRET
    test_client_access_token = config.CLIENT_ACCESS_TOKEN 
    assert client_id == test_client_id  and client_secret == test_client_secret  and client_access_token == test_client_access_token  

def test_search():
    client_id, client_secret, client_access_token = lyrics.load_credentials()
    search_term = "make some music make some money"
    search_return = lyrics.search(search_term, client_access_token)
    len(search_return) == 10
    