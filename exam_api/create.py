import json
import logging
import boto3
import os
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('QUESTIONS_TABLE')

logger = logging.getLogger('exam-api')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    logger.info(f'event->{event}')
    
    question = json.loads(event['body'])        
    question['id'] = str(uuid.uuid4())
    
    table = dynamodb.Table(table_name)
    response = table.put_item(TableName=table_name, Item=question)
    print(response)
    return{
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({'message': 'Question-Answer Created'})
    }
