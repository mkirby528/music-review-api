import simplejson as json
import re
import boto3
import os
import spotipy
import src.constants as constants
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from src.utils.response_utils import format_response
from src.utils.spotify import build_album_object
from src.albums.get_albums import get_review_by_id, get_all_reviews
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

    if method == "GET" and re.fullmatch(constants.GET_ALL_ALBUMS_PATH_REGEX, path):
        print("Getting all album reviews")
        response = get_all_reviews(table, query_params)
        return format_response(200, response)
    if method == "GET" and re.fullmatch(constants.GET_ALBUM_BY_ID_PATH_REGEX, path):
            print("Getting album review by album id")
            album_id = path_paramaters.get("albumID", "")
            if not album_id: 
                return format_response(404, {})
            response = get_review_by_id(table, album_id)
            return format_response(200, response)
    
    if method == "POST":
        album_item = json.loads(body)
        album_object = build_album_object(spotify, album_item)
        print("================")
        print(album_object)
        print("================")
        response = table.put_item(Item=album_object)
        return format_response(201, response)

    if method == "PATCH":
        album_id = path_paramaters.get("albumID", "")
        if not album_id:
            return (400, "No albumID provided.")
        if bool(re.search(constants.ADD_VINYL_PATH_REGEX, path)):
            return format_response(200, addVinylRecord(album_id))
        else:
            update_fields = json.loads(body)
            album = update_album(album_id, update_fields)

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


def addVinylRecord(album_id):
    album = update_album(album_id, {"HaveVinyl": True})
    if album:
        return True


def create_album_record(album):
    title = album["Title"]
    artist = album["Artist"]
    album["Type"] = "ALBUM"
    album = add_album_metadata(album, title, artist)
    #
    return album


def update_album(album_id, fields_to_update):
    album = table.query(KeyConditionExpression=Key(
        'id').eq(album_id))["Items"][0]
    print(f"Updating album `{album['Title']}`... ")
    print(f"Fields to update: {fields_to_update}")
    update_expressions = []
    expression_attribute_values = {}
    count = 0
    for field, value in fields_to_update.items():
        if field not in album:
            print(f"Field `{field}` not present on original object")
            return False
        update_expressions.append(f'{field}= :var{count}')
        expression_attribute_values[f":var{count}"] = value
        count += 1
    return table.update_item(
        Key={
            'id': album_id
        },
        UpdateExpression="SET " + ",".join(update_expressions),
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="ALL_NEW"
    )


  


