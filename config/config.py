token: str = "NzMzMzQ4MDg0NzEyNzM0NzIw.XxB1oA.MR2XoAA-Oe3TxKOI0lPjmKVoUbY"
CLIENT_ID = '9bghKCR_r63trsjHm5xKOlX-ao14wm-WZjp3YtYliI9zkeL04U8phKvHWh93ve27'
CLIENT_SECRET = 'x3tpg54Pfd2-2McPxjFIbco9L95fKnQmDTglS6Bv8QrwJhydpoUD54El1EvRqNu1BTQP8eDQ7JAviFMyqBNLdQ'
CLIENT_ACCESS_TOKEN = 'Guxci2VxlB5aOZ5O5RXUARnBBkfyNcyiE02UI_kGQz-H2Am1me6q72bYXHlJZ4ue'

DEFAULT_NICKNAME = "MSc Development Project 2020"

STARTUP_MESSAGE = "Starting Bot..."
STARTUP_COMPLETE_MESSAGE = "Startup Complete"

NO_GUILD_MESSAGE = 'Error: Please join a voice channel or enter the command in guild chat'
NOT_CONNECTED_MESSAGE = "Error: Bot not connected to any voice channel"
CHANNEL_NOT_FOUND_MESSAGE = "Error: Could not find channel "
DEFAULT_CHANNEL_JOIN_FAILED = "Error: Could not join the default voice channel"
INVALID_INVITE_MESSAGE = "Error: Invalid invitation link"

ADD_MESSAGE_1 = """```To add this bot to your own Server, click the following link:
                ```\n<https://discordapp.com/oauth2/authorize?client_id="""
ADD_MESSAGE_2 = "&scope=bot>"


DEFAULT_VOLUME = 7

INFO_HISTORY_TITLE = "Songs Played:"
QUEUE_TITLE = "Song Queue:"
MAX_HISTORY_LENGTH = 10
MAX_TRACKNAME_HISTORY_LENGTH = 15

SONGINFO_UPLOADER = "Uploader: "
SONGINFO_DURATION = "Duration: "
SONGINFO_SECONDS = "s"
SONGINFO_LIKES = "Likes: "
SONGINFO_DISLIKES = "Dislikes: "

HELP_LYRICPLAY_SHORT = "Finds and plays the song from lyrics. .lyricplay <lyrics>"
HELP_LYRICPLAY_LONG = "Uses the provided lyrics to search up a song and play it in a voice channel"
HELP_LYRICSEARCH_SHORT = "Shows list of songs based on the lyrics provided. .lyricsearch <lyrics>"
HELP_LYRICSEARCH_LONG = "Uses the lyrics provided to search for linked songs and displays the results in a list"
#HELP_GETLYRICS_SHORT = ""
#HELP_GETLYRICS_LONG = ""

HELP_ADDBOT_SHORT = "Add Bot to another server"
HELP_ADDBOT_LONG = "Gives you the link for adding this bot to another server of yours."
HELP_CC_SHORT = "Change voicechannel. .cc <Channel Name>"
HELP_CC_LONG = "Switches the bot to another voicechannel."
HELP_CONNECT_SHORT = "Connect bot to voicechannel.  .connect <Channel Name>"
HELP_CONNECT_LONG = "Connects the bot to a given voice channel and the voice client associated with that client."
HELP_SUMMON_SHORT = ""
HELP_SUMMON_LONG = ""
HELP_DISCONNECT_SHORT = "Disconnects bot from voicechannel."
HELP_DISCONNECT_LONG = ""

HELP_HISTORY_SHORT = "Show history of songs"
HELP_HISTORY_LONG = "Shows the " + str(MAX_TRACKNAME_HISTORY_LENGTH) + " last played songs."
HELP_QUEUE_LONG = "Shows the list of songs in the queue"
HELP_QUEUE_SHORT = "Shows upcoming songs."
HELP_PAUSE_SHORT = "Pause Music"
HELP_PAUSE_LONG = "Pauses the AudioPlayer. Playback can be continued with the resume command."
HELP_PREV_SHORT = "Go back one Song"
HELP_PREV_LONG = "Plays the previous song again."
HELP_RESUME_SHORT = "Resume Music"
HELP_RESUME_LONG = "Resumes the AudioPlayer."
HELP_SKIP_SHORT = "Skip a song"
HELP_SKIP_LONG = "Skips the currently playing song and goes to the next item in the queue."
HELP_SONGINFO_SHORT = "Info about current Song"
HELP_SONGINFO_LONG = "Shows details about the song currently being played and posts a link to the song."
HELP_SPOTIFY_SHORT = "Play song from Spotify.  Use .help spotify for more."
HELP_SPOTIFY_LONG = ("Play song from Spotify.  Whoever uses the command must be listening to a song on Spotify AND have Spotify linked to their Discord account.  If the command sender doesn't have a Spotify account linked to their Discord AND also be listening to a song on Spotify.  This will not work.")
HELP_STOP_SHORT = "Stop Music"
HELP_STOP_LONG = "Stops the AudioPlayer and clears the songqueue"
HELP_VOL_SHORT = "Change volume.  1-200 (200 very loud)"
HELP_VOL_LONG = "Changes the volume of the AudioPlayer. Argument specifies the % to which the volume should be set."
HELP_YT_SHORT = "Play song from Youtube. .play <query/link>"
HELP_YT_LONG = ("Plays the audio of a Youtube video. Argument can be a direct YouTube link, the title of a specific video or a generalised search.")
