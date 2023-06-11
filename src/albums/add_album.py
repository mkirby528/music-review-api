def add_album_to_db(table, album):
    album["ArtistsString"] = ", ".join(album["Artists"])
    return table.put_item(Item=album)
