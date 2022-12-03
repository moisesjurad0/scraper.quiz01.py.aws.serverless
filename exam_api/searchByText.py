import json

import simplejson as json
from boto3.dynamodb.conditions import Key, Attr
import app

logger = app.logger
dynamodb = app.dynamodb
table_name = app.table_name


def lambda_handler(event, context):

    logger.info(f'event->{event}')

    request_json = json.loads(event['body'])
    table = dynamodb.Table(table_name)

    response = None

    for i in ('id', 'UUID', 'question', 'answer', 'text'):
        logger.info(f'i->{i}')
        try:
            if request_json[i] is not None:
                if i in ('id'):
                    response = table.query(
                        KeyConditionExpression=Key(i).eq(request_json[i]))
                elif i in ('UUID', 'question', 'answer'):
                    response = table.scan(
                        FilterExpression=Attr(i).contains(request_json[i]))
                elif i == 'text':
                    response = table.scan(
                        FilterExpression=Attr('question').contains(request_json[i]) or
                        Attr('answer').contains(request_json[i]))
            logger.info(f'response->{response}')
            break
        except KeyError as e:
            logger.warning(e, exc_info=True)

    return{
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
