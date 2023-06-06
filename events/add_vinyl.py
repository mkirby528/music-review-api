import simplejson as json
body = {
    "Rating": 10,
}

event = {
    "path": "/albums/abc123/addVinyl",
    "httpMethod": "PATCH",
    "headers": {},
    "multiValueHeaders": {},
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": {
        "albumID": "abc123"
    },
    "stageVariables": None,
    "requestContext": {},
    "body": json.dumps(body),
    "isBase64Encoded": False
}
