"""Modulo de busqueda por id.

Returns:
    _type_: _description_
"""
import simplejson as json
from boto3.dynamodb.conditions import Key
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

    table = dynamodb.Table(table_name)
    question_id = event['pathParameters']['id']

    response = table.query(KeyConditionExpression=Key('id').eq(question_id))

    logger.info(f'response->{response}')

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }
