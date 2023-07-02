import simplejson as json
import re
import boto3
import os
import spotipy
import src.constants as constants
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from src.utils.response_utils import format_response
from src.utils.jwt import decode
from src.albums.get_albums import get_review_by_id, get_all_reviews
from src.albums.search_spotify import search_album
from src.albums.update_album import update_album, addVinylRecord
from src.albums.add_album import add_album_to_db
from urllib.parse import unquote

import src.constants as constants
if os.getenv("TABLE_NAME") is None:
    load_dotenv("./.env")


auth_manager = SpotifyClientCredentials()
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
dynamodb_resource = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb_resource.Table(TABLE_NAME)


def lambda_handler(event, context):
    # Read and process request elements
    path = event.get('path', '')
    path_paramaters = event.get("pathParameters", {})
    method = event.get('httpMethod', '').upper()
    headers = event.get('headers', {})
    query_params = event.get('queryStringParameters')
    body = event.get('body', {})

    if not query_params:
        query_params = {}
    print(f'Method: {method}')
    print(f"Path: {path}")
    print(f"Path Parameters: {path_paramaters}")
    print(f"Headers: {headers}")
    print(f"Query Paramaters: {query_params}")
    print(f"Body: {body}")

    # GET /albums
    if method == "GET" and re.fullmatch(constants.GET_ALL_ALBUMS_PATH_REGEX, path):
        print("Getting all album reviews")
        response = get_all_reviews(table, query_params)
        return format_response(200, response)
    # GET /albums/:albumId
    if method == "GET" and re.fullmatch(constants.GET_ALBUM_BY_ID_PATH_REGEX, path):
        album_id = path_paramaters.get("albumID", "")
        if not album_id:
            return format_response(404, {})
        response = get_review_by_id(table, album_id)
        return format_response(200, response)
     # GET /albums/spotfiy/search
    if method == "GET" and re.fullmatch(constants.SPOTIFY_SEARCH_PATH_REGEX, path):
        title = unquote(query_params.get("Title", "")).strip()
        artist = unquote(query_params.get("Artist", "")).strip()
        response = search_album(spotify, title, artist)
        return format_response(200, response)
     # POST /albums/
    if method == "POST":
        decoded_token = decode(headers["Authorization"])
        album_item = json.loads(body)
        album_item["ReviewerId"] = decoded_token["sub"]
        return format_response(201, add_album_to_db(table, album_item))
    if method == "PATCH":
        album_id = path_paramaters.get("albumID", "")
        if not album_id:
            return (400, "No albumID provided.")
        # PATCH /albums/:albumId/addVinyl
        if bool(re.match(constants.ADD_VINYL_PATH_REGEX, path)):
            return format_response(200, addVinylRecord(table, album_id))
        # PATCH /albums/:albumId
        else:
            update_fields = json.loads(body)
            album = update_album(table, album_id, update_fields)
            return format_response(200, album)

    if method == "DELETE":
        album_id = path_paramaters.get("albumID", "")
        if not album_id:
            return (400, "No albumID provided.")
        response = table.delete_item(
            Key={
                'id': album_id
            }
        )
        return format_response(200, response)
