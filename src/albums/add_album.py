def add_album_to_db(table, album):
    print(album)
    return table.put_item(Item=album)
