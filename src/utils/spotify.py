from datetime import datetime, date
import json


def build_album_object(spotipy_client, album):
    title = album["Title"].strip()
    album["Title"] = title
    artist = album["Artist"].strip()
    query_string = f"{title} artist:{artist}"
    results = spotipy_client.search(
        q=query_string, type='album')
    album_id = results["albums"]["items"][0]["id"]
    album = _add_metadata_from_spotify(spotipy_client, album, album_id)
    album["Tracks"] = _get_album_tracks(spotipy_client, album_id)
    print(json.dumps(album, indent=2))


def _add_metadata_from_spotify(spotipy_client, album, id):
    album["id"] = id
    album_response = spotipy_client.album(id)
    spotify_album = album_response
    album_response = {}
    artists = []
    for artist in spotify_album["artists"]:
        artists.append(artist["name"])
    del album["Artist"]
    album["Artists"] = artists
    album["SpotifyURI"] = spotify_album["external_urls"]["spotify"]
    album["Images"] = {}
    album["Images"]["lg"] = spotify_album["images"][0]["url"]
    album["Images"]["md"] = spotify_album["images"][1]["url"]
    album["Images"]["sm"] = spotify_album["images"][2]["url"]
    album["NumberOfTracks"] = spotify_album["total_tracks"]

    album["ReleaseDate"] = _try_parsing_date(spotify_album["release_date"])
    album["ReleaseYear"] = album["ReleaseDate"][:4]

    if not "DateListened" in album:
        album["DateListened"] = date.today().isoformat()
    if not "HaveVinyl" in album:
        album["HaveVinyl"] = False
    album["Type"] = "ALBUM"
    return (album)


def _get_album_tracks(spotipy_client, id):
    tracks_response = spotipy_client.album_tracks(id)
    tracks = []
    for track in tracks_response["items"]:
        tracks.append(track["name"])
    return tracks


def _try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%Y', '%Y-%m'):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    raise ValueError('no valid date format found')
