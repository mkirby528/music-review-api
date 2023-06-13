import random
import openai


def generate_review(album: dict) -> str:
    title = album["Title"]
    artist = album["ArtistsString"]
    rating = album["Rating"]

    rand_value = (random.randint(0, 9))
    style = ''
    if rand_value < 2:
        style = random.choice(["Yoda", "Shakespeare", "a Valley Girl",
                               "a Scottish Person", "James Bond", "a Cowboy",
                               "a Haiku", "a Chef", "A robot", "a comedian",
                               "a sailor", "a frat bro"])
    else:
        style = "a music critic"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Write a review for the album '{title}' by the artist '{artist}' \
                                        with a rating of {rating} out of 10 in the style of {style}. Include specific references \
                                        to the album and don't be afraid to use humor. \
                                        Begin straight into the review without a title."}
        ]
    )

    review = completion.choices[0].message["content"]
    return review
