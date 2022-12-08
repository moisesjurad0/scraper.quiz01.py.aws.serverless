"""_summary_.

Returns:
    _type_: _description_
"""
import json
import uuid
import app

logger = app.logger
dynamodb = app.dynamodb
table_name = app.table_name


def lambda_handler(event, context):
    """_summary_.

    Args:
        event (_type_): _description_
        context (_type_): _description_

    Returns:
        _type_: _description_
    """
    logger.info(f'event->{event}')

    question = json.loads(event['body'])
    question['id'] = uuid.uuid4().hex

    table = dynamodb.Table(table_name)
    response = table.put_item(TableName=table_name, Item=question)

    logger.info(f'response->{response}')

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({
            'message': 'Question-Answer Created',
            'id': question['id']})
    }
