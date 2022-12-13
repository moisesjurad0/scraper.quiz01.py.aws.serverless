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

    request = json.loads(event['body'])
    table = dynamodb.Table(table_name)

    my_attribs = (
        'question',  # string
        'question_type',  # string
        'answer',  # string
        'correct'  # boolean
    )

    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#querying-and-scanning
    # You are also able to chain conditions together using the logical operators: & (and), | (or), and ~ (not).
    # For example, this scans for all users whose first_name starts with J and whose account_type is super_user:
    response = table.scan(
        FilterExpression=(
                Attr(my_attribs[0]).contains(request[my_attribs[0]]) &
                Attr(my_attribs[1]).contains(request[my_attribs[1]]) &
                Attr(my_attribs[2]).contains(request[my_attribs[2]]) &
                Attr(my_attribs[3]).eq(request[my_attribs[3]])
        )
    )
    logger.info(f'response->{response}')

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
