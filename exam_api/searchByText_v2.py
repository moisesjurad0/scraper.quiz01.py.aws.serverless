import logging
import os

import boto3
import simplejson as json
from boto3.dynamodb.conditions import Attr

logger = logging.getLogger('exam-api')
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('QUESTIONS_TABLE')


def lambda_handler(event, context):
    logger.info(f'event->{event}')

    request_json = json.loads(event['body'])
    table = dynamodb.Table(table_name)

    response = None

    my_attribs = (
        'question',  # string
        'question_type',  # string
        'answer',  # string
        'correct'  # boolean
    )

    # try:
    response = table.scan(
        FilterExpression=(
                Attr(my_attribs[0]).contains(request_json[my_attribs[0]]) and
                Attr(my_attribs[1]).contains(request_json[my_attribs[1]]) and
                Attr(my_attribs[2]).contains(request_json[my_attribs[2]]) and
                Attr(my_attribs[3]).eq(request_json[my_attribs[3]])
        )
    )
    logger.info(f'response->{response}')
    # except KeyError as e:
    # logger.warning(e, exc_info=True)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
