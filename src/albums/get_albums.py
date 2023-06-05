from boto3.dynamodb.conditions import Key

def get_review_by_id(table, album_id: str) -> dict:
    print(f"Getting album review by album id: {album_id}")
    response = table.query(KeyConditionExpression=Key('id').eq(album_id))
    items = response["Items"]
    if not items:
        return None
    return items[0]

def get_all_reviews(table, query_params, limit:int = None):
    print("Getting all album reviews")
    albums = table.scan()["Items"]
    
    sort_key = query_params.get("sort_key", "Title")
    sort_order = query_params.get("sort_order", "asc")
    is_descending = False
    
    if sort_key not in ("Title", "Rating", "Artist", "DateListened", "ReleaseDate"):
        return False
    if sort_order.lower() in ("desc", "descending"):
        is_descending = True
    if sort_key == "Rating":
        return sorted(albums, key=lambda d: int(d[sort_key]), reverse=is_descending)
    
    return sorted(albums, key=lambda d: d[sort_key], reverse=is_descending)