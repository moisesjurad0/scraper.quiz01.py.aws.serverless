import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('QUESTIONS_TABLE')


def lambda_handler(event, context):
    question = json.loads(event['body'])
    table = dynamodb.Table(table_name)
    response = table.put_item(TableName=table_name, Item=question)
    print(response)
    return{
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'message': 'Order Created'})
    }
