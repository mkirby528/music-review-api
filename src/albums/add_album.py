def add_album_to_db(table, album):
    album["ArtistsString"] = ", ".join(get_artists(album))
    return table.put_item(Item=album)


def get_artists(album):
    artists = []
    for artist in album["artists"]:
        artists.append(artist["name"])
    return artists
