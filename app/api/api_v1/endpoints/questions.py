from fastapi import APIRouter
from typing import Optional  # , List
import logging
import os
import boto3
from typing import Union
from pydantic import BaseModel  # , PositiveInt, Field
from boto3.dynamodb.conditions import Key, Attr
# from boto3.dynamodb.conditions import Key, logical_and
from enum import Enum
from functools import reduce


router = APIRouter()
logger = logging.getLogger(os.environ.get('APP_NAME'))
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('API_TABLE_PYSICAL_ID')


class QuestionType(str, Enum):
    CHECK = 'CHECK'
    RADIO = 'RADIO'
    RADIO_BOOL = 'RADIO_BOOL'


class Question(BaseModel):
    id: str
    exam_number: int  # PositiveInt
    question_type: str
    answer_text: str
    is_correct: bool
    last_modified: str


class QuestionQuery(BaseModel):
    id: Optional[str] = None
    exam_number: Optional[int] = None  # Optional[PositiveInt]
    question_type: Optional[str] = None
    answer_text: Optional[str] = None
    is_correct: Optional[Union[bool, None]] = None
    last_modified: Optional[str] = None


@router.get("/")
async def root():
    return {"message": "Get Questions!"}


@router.get("/{id}/{answer_text}")
def read_item(id: str, answer_text: str):
    table = dynamodb.Table(table_name)
    # response = table.query(KeyConditionExpression=Key('id').eq(id))
    # response = table.query(Key={'id': id,'answer_text': answer_text})

    response = table.query(
        KeyConditionExpression=(
            Key('id').eq(id) &
            Key('answer_text').eq(answer_text)
        )
    )

    logger.info(f'response=>{response}')
    # return {
    #     'statusCode': 200,
    #     'headers': {},
    #     'body': json.dumps(response['Items'])
    # }
    return response


@router.delete("/{id}/{answer_text}")
def delete_item(id: str, answer_text: str):
    table = dynamodb.Table(table_name)
    # response = table.query(KeyConditionExpression=Key('id').eq(id))
    response = table.delete_item(Key={'id': id, 'answer_text': answer_text})
    logger.info(f'response=>{response}')
    # return {
    #     'statusCode': 200,
    #     'headers': {},
    #     'body': json.dumps(response['Items'])
    # }
    return response


@router.put("/")
def put_item(item: Question):
    table = dynamodb.Table(table_name)
    response = table.put_item(Item=item.dict())
    logger.info(f'response=>{response}')
    # return {
    #     'statusCode': 201,
    #     'headers': {},
    #     'body': json.dumps({
    #         'message': 'Item Created',
    #         'id': item.id})
    # }
    return response


@router.post("/contains")
def search_items(question: QuestionQuery):

    table = dynamodb.Table(table_name)
    filter_conditions = []

    if question:

        for i_prop_name, i_prop_value in question.dict().items():

            if i_prop_value is not None:

                logger.info(f'i:{i_prop_name}=>{i_prop_value}')

                if i_prop_name in {'id', 'answer_text'}:  # KEY begins_with
                    filter_conditions.append(
                        Key(i_prop_name).begins_with(i_prop_value))
                elif i_prop_name in {'question_type', 'is_correct', 'exam_number'}:  # ATTR eq
                    filter_conditions.append(
                        Attr(i_prop_name).eq(i_prop_value))
                else:  # ATTR else
                    filter_conditions.append(
                        Attr(i_prop_name).begins_with(i_prop_value))

    if filter_conditions:
        response = table.scan(
            FilterExpression=reduce(lambda x, y: x & y, filter_conditions))
    else:
        # No filters provided, retrieve all items
        response = table.scan()

    logger.info(f'm01.response=>{response}')
    return response
