"""Modulo de busqueda por texto v1.

Returns:
    _type_: _description_
"""
# import json

import simplejson as json
from boto3.dynamodb.conditions import Key, Attr
import app

logger = app.logger
dynamodb = app.dynamodb
table_name = app.table_name


def lambda_handler(event, context):
    """Metodo de entrada.

    Args:
        event (_type_): _description_
        context (_type_): _description_

    Returns:
        _type_: _description_
    """
    logger.info(f'event->{event}')

    request_json = json.loads(event['body'])
    table = dynamodb.Table(table_name)

    response = None

    for i in (
        'id',
        'uuid',
        'question',
        'question_type',
        'answer',
        'text',
            'correct'):
        logger.info(f'i->{i}')
        try:
            if request_json[i] is not None:
                if i in ('id'):
                    response = table.query(
                        KeyConditionExpression=Key(i).eq(request_json[i]))
                elif i in ('uuid', 'question', 'question_type', 'answer'):
                    response = table.scan(
                        FilterExpression=Attr(i).contains(request_json[i]))
                elif i == 'text':
                    response = table.scan(FilterExpression=(
                        Attr('question').contains(request_json[i]) or
                        Attr('answer').contains(request_json[i])))
                elif i == 'correct':
                    response = table.scan(
                        FilterExpression=Attr(i).eq(request_json[i]))
                logger.info(f'response->{response}')
                break
        except KeyError as e:
            logger.warning(e, exc_info=True)

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
