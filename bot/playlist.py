from collections import deque

from config import config


class Playlist:

    def __init__(self):
        # Stores the ytlinks os the songs in queue and the ones already played
        self.playqueue = deque()
        self.playhistory = deque()

        # A seperate history that remembers the names of the tracks that were played
        self.trackname_history = deque()
        self.playqueuename_history = deque()

    def __len__(self):
        return len(self.playqueue)

    def add_name_history(self, trackname):
        self.trackname_history.append(trackname)
        if len(self.trackname_history) > config.MAX_TRACKNAME_HISTORY_LENGTH:
                self.trackname_history.popleft()

    def add_name_queue(self, trackname):
        self.playqueuename_history.append(trackname)
        if len(self.playqueuename_history) > config.MAX_TRACKNAME_HISTORY_LENGTH:
                self.playqueuename_history.popright()

    def add(self, track):
        self.playqueue.append(track)

    def next(self):
        song_played = self.playqueue.popleft()
        if song_played != "Dummy":
            self.playhistory.append(song_played)
            if len(self.playhistory) > config.MAX_HISTORY_LENGTH:
                self.playhistory.popleft()
        if len(self.playqueue) == 0:
            return None
        return self.playqueue[0]

    def prev(self):
        if len(self.playhistory) == 0:
            dummy = "DummySong"
            self.playqueue.appendleft(dummy)
            return dummy
        self.playqueue.appendleft(self.playhistory.pop())
        return self.playqueue[0]

    def empty(self):
        self.playqueue.clear()
        self.playhistory.clear()
