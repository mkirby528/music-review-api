import simplejson as json
body = {
    "Rating": 10,
    "HaveVinyl": True,
}

event = {
    "resource": "/albums/\{albumID\}",
    "path": "/albums/3DGQ1iZ9XKUQxAUWjfC34w",
    "httpMethod": "PATCH",
    "headers": {},
    "multiValueHeaders": {},
    "queryStringParameters": None,
    "multiValueQueryStringParameters": None,
    "pathParameters": {
        "albumID": "3DGQ1iZ9XKUQxAUWjfC34w"
    },
    "stageVariables": None,
    "requestContext": {},
    "body": json.dumps(body),
    "isBase64Encoded": False
}
