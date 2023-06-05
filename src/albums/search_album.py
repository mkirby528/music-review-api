def search_album(spotipy_client, album):
    if "Title" not in album:
        return False
    if "Artist" not in album: 
        return False
    title = album["Title"].strip()
    album["Title"] = title
    artist = album["Artist"].strip()
    query_string = f"{title} artist:{artist}"
    results = spotipy_client.search(
        q=query_string, type='album')
    print(results)

