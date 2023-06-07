from urllib.parse import quote
from datetime import datetime, date


def search_album(spotipy_client, title, artist):
    print(f"Searching spotify with Title `{title}` and artist `{artist}`")
    query_string = f"{title} artist:{artist}"
    print('query string', query_string)
    response = []
    try:
        results = spotipy_client.search(
            q=query_string, type='album')
        for spotify_album in results["albums"]["items"]:
            album = {
                "id": spotify_album["id"],
                "Title": spotify_album["name"],
                "Artists": get_artists(spotify_album),
                "ArtistsString": ", ".join(get_artists(spotify_album)),
                "SpotifyURI": spotify_album["external_urls"]["spotify"],
                "Images": {
                    "lg": spotify_album["images"][0]["url"],
                    "md": spotify_album["images"][1]["url"],
                    "sm": spotify_album["images"][2]["url"]
                },
                "NumberOfTracks": spotify_album["total_tracks"],
                "ReleaseDate": _try_parsing_date(spotify_album["release_date"]),
                "ReleaseYear": _try_parsing_date(spotify_album["release_date"])[:4],
                "DateListened": date.today().isoformat(),
                "Type": "ALBUM",
                "Tracks":  _get_album_tracks(spotipy_client, spotify_album["id"])
            }
            response.append(album)
    except Exception as e:
        print(f'error: {e}')
    return response


def search_album_by_spotify_id(spotipy_client, id):
    print(f"Getting spotify album by id `{id}`")
    album_response = spotipy_client.album(id)
    return album_response


def get_artists(album):
    artists = []
    for artist in album["artists"]:
        artists.append(artist["name"])
    return artists


def _try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%Y', '%Y-%m'):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def _get_album_tracks(spotipy_client, id):
    tracks_response = spotipy_client.album_tracks(id)
    tracks = []
    for track in tracks_response["items"]:
        tracks.append(track["name"])
    return tracks
