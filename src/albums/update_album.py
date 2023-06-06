from boto3.dynamodb.conditions import Key


def update_album(table, album_id, fields_to_update):
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


def addVinylRecord(table, album_id):
    album = update_album(table, album_id, {"HaveVinyl": True})
    if album:
        return True
