from playlists_gen import Playlist_gen
from enum import Enum

class QuackLocationType(Enum):
    unknown = 0
    church = 1
    education = 2
    cemetery = 3
    forest = 4
    beach = 5
    urban = 6
    night_life = 7

def main(args):
    playlist_gen = Playlist_gen(args[0])
    words = playlist_gen.get_searchwords(1)
    playlist_gen.get_playlist(words)

if __name__ == "__main__":
    main()
