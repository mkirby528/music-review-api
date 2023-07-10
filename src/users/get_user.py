from boto3.dynamodb.conditions import Key

def get_user_by_id(table, user_id: str) -> dict:
    print(f"Getting user by id id: {user_id}")
    response = table.query(KeyConditionExpression=Key('id').eq(user_id))
    print(response)
    items = response["Items"]
    
    if not items:
        return None
    return items[0]

