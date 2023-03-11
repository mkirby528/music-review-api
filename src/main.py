import simplejson as json
import boto3
import os
import spotipy
import src.constants as constants
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
from boto3.dynamodb.conditions import Key
from src.utils.response_utils import format_response


if os.getenv("TABLE_NAME") is None:
    load_dotenv("./.env")


auth_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
dynamodb_resource = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb_resource.Table(TABLE_NAME)


def lambda_handler(event, context):
    print(constants.ALBUM_REGEX_PATH)
    print(f"Recieved event: \n {event}")
    path = event.get('path', '')
    path_paramaters = event.get("pathParameters", '')
    method = event.get('httpMethod', '').upper()
    headers = event.get('headers', {})
    query_params = event.get('queryStringParameters')
    if not query_params:
        query_params = {}
    print(f'Method: {method}')
    print(f"Path: {path}")
    print(f"Path Parameters: {path_paramaters}")
    print(f"Headers: {headers}")
    print(f"Query Paramaters: {query_params}")

    if method == "GET":
        response = get_all_albums(query_params)
        if not response:
            return format_response(404)
        return format_response(200, response)

    if method == "POST":
        body = event.get('body', {})
        album_item = json.loads(body)
        dynamo_response = create_album_record(album_item)
        return format_response(201, dynamo_response)

    if method == "DELETE":
        print("DELETE request")

    if method == "PATCH":
        print("PATCH request")


def create_album_record(album):
    title = album["Title"]
    artist = album["Artist"]
    album["Type"] = "ALBUM"
    album = add_album_metadata(album, title, artist)
    print(album)
    response = table.put_item(Item=album)
    return (response)


def get_all_albums(query_params):
    albums = table.scan()["Items"]
    sort_key = query_params.get("sort_key", "Title")
    sort_order = query_params.get("sort_order", "asc")
    is_descending = False
    if sort_key not in ("Title", "Rating", "Artist", "DateListened", "ReleaseDate"):
        return False
    if sort_order.lower() in ("desc", "descending"):
        is_descending = True
    return sorted(albums, key=lambda d: d[sort_key], reverse=is_descending)


def get_album(query_params):
    if query_params and "Title" in query_params:
        title = query_params["Title"]
        response = table.query(KeyConditionExpression=Key('Title').eq(title))
        items = response["Items"]
        if not items:
            return None
        return items[0]


def add_album_metadata(album, title, artist):
    query_string = f"{title} artist:{artist}"
    print(query_string)
    results = spotify.search(
        q=query_string, type='album')
    print(results)
    if len(results['albums']['items']) == 0:
        query_string = f"{title}"
        results = spotify.search(
            q=query_string, type='album')
    seach_result = results['albums']['items'][0]
    spotify_album = spotify.album(seach_result["id"])
    album["id"] = spotify_album["id"]
    if spotify_album["release_date_precision"] == "day":
        album["ReleaseDate"] = datetime.strptime(
            spotify_album["release_date"], '%Y-%m-%d').strftime('%m/%d/%Y')
    else:
        album["ReleaseDate"] = spotify_album["release_date"]
    album["SpotifyURI"] = spotify_album["external_urls"]["spotify"]
    album["Images"] = {}
    album["Images"]["lg"] = spotify_album["images"][0]["url"]
    album["Images"]["md"] = spotify_album["images"][1]["url"]
    album["Images"]["sm"] = spotify_album["images"][2]["url"]
    album["NumberOfTracks"] = spotify_album["total_tracks"]
    if not "DateListened" in album:
        album["DateListened"] = date.today().strftime("%m/%d/%Y")
    if not "HaveVinyl" in album:
        album["HaveVinyl"] = False
    return album
