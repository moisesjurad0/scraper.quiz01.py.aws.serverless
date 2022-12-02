import json
import logging
import os

import boto3
import simplejson as json
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('QUESTIONS_TABLE')

logger = logging.getLogger('exam-api')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    logger.info(f'event->{event}')
    
    
    question = json.loads(event['body'])
    table = dynamodb.Table(table_name)
    
    response=None
    if question["id"] is not None:
        response = table.query(KeyConditionExpression=Key('id').eq(question["id"]))
    if question["text"] is not None:
        response = table.scan(FilterExpression=Attr('question').contains(question["text"]) or Attr('answer').contains(question["text"]))

    return{
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }

