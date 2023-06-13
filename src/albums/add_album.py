from src.openai.album_review import generate_review


def add_album_to_db(table, album):
    album["ArtistsString"] = ", ".join(album["Artists"])
    review = generate_review(album)
    album["OpenAIReview"] = review
    return table.put_item(Item=album)
