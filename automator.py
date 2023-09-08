from youtube_client import YouTubeClient
from spotify_client import SpotifyClient


def automate():
    # Retrieve youtube playlists
    youtube_client = YouTubeClient('./client_secret_youtube.json')
    playlists = youtube_client.get_youtube_playlists()

    # Get user's playlist name of choice
    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice_input = int(input("Please type in the playlist number: "))
    user_playlist_selection = playlists[choice_input]
    print(f"Generating playlist from {user_playlist_selection}")

    # Retrieve song details for playlist videos
    songs= youtube_client.get_playlist_vids(user_playlist_selection.id)
    print(f"Adding {len(songs)}")

    # Search the song on Spotify using the details
    spotify_client = SpotifyClient()
    for song in songs:
        spotify_song_id = spotify_client.search_for_song(song.artist, song.track)
        if spotify_song_id:
            added_song = spotify_client.add_to_playlist(spotify_song_id)
            if added_song:
                print(f"Successfully added {song.artist}")


if __name__ == '__main__':
    automate()
