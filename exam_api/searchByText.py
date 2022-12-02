import json

import simplejson as json
from boto3.dynamodb.conditions import Key, Attr
import app

logger = app.logger
dynamodb = app.dynamodb
table_name = app.table_name

def lambda_handler(event, context):
    
    logger.info(f'event->{event}')
    
    
    question = json.loads(event['body'])
    table = dynamodb.Table(table_name)
    
    response=None
    if question["id"] is not None:
        response = table.query(KeyConditionExpression=Key('id').eq(question["id"]))
        logger.info(f'response->{response}')
    if question["text"] is not None:
        response = table.scan(FilterExpression=Attr('question').contains(question["text"]) or Attr('answer').contains(question["text"]))
        logger.info(f'response->{response}')

    return{
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }

