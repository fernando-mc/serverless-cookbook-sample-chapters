import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])


def handler(event, context):
    object_id = event['pathParameters']['id']
    result = table.get_item(
        Key={
            'pk': object_id
        }
    )
    response = {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps(result['Item'])
    }
    return response
