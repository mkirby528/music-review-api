import boto3
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

if os.getenv("TABLE_NAME") is None:
    load_dotenv("./.env")


auth_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
dynamodb_resource = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb_resource.Table(TABLE_NAME)

albums = table.scan()["Items"]
for album in albums:
    # if not "ReviewerId" in album:
    print(album["Title"])
    album["Rating"] = int(album["Rating"])
    album["ReviewerId"] = "b428f458-e081-709f-b435-c7fae16f6f6b"
    table.put_item(Item=album)
    
