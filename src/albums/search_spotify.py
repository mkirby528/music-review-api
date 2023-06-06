from urllib.parse import quote


def search_album(spotipy_client, title, artist):
    print(f"Searching spotify with Title `{title}` and artist `{artist}`")
    query_string = f"{title} artist:{artist}"
    print('query string', query_string)
    response = []
    try:
        results = spotipy_client.search(
            q=query_string, type='album')
        for album in results["albums"]["items"]:
            response.append(album)
    except Exception as e:
        print(f'error: {e}')
    return response


def search_album_by_spotify_id(spotipy_client, id):
    print(f"Getting spotify album by id `{id}`")
    album_response = spotipy_client.album(id)
    return album_response
