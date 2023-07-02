from src.openai.album_review import generate_review


def add_album_to_db(table, album):
    album["ArtistsString"] = ", ".join(album["Artists"])
    album["OpenAIReview"] = generate_review(album)
    return table.put_item(Item=album)
