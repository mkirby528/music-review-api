import simplejson as json


def format_response(status_code, response_body={}):
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }
