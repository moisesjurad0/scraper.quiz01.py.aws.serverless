from fastapi import APIRouter
from typing import List, Optional
import logging
import os
import boto3
from typing import Union
import json
# import simplejson as sjson
from typing import Union
from pydantic import BaseModel, Field
from boto3.dynamodb.conditions import Key, Attr
# from boto3.dynamodb.conditions import Key, logical_and
from enum import Enum
from functools import reduce


router = APIRouter()
logger = logging.getLogger(os.environ.get('APP_NAME'))
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('API_TABLE_PYSICAL_ID')


class Answer(BaseModel):
    answer_text: str = 'Celeste'
    is_correct: Union[bool, None] = False


class QuestionType(str, Enum):
    CHECK = 'CHECK'
    RADIO = 'RADIO'
    RADIO_BOOL = 'RADIO_BOOL'


class Question(BaseModel):
    # id: str
    id: str = '¿De que colores es un Arco Iris?'
    # question_text: str = '¿De que colores es un Arco Iris?'
    question_type: str = 'CHECK'  # CHANGE THIS TO QuestionType, set default to CHECK
    last_modified: str = '2023-09-214T13:41:38.446131'
    # answers: Optional[List[Answer]]
    # answers: Optional[List[Answer]] = List[Answer(), Answer()]
    answers: Optional[List[Answer]] = Field(default=[Answer(), Answer()])


@router.get("/")
async def root():
    return {"message": "Get Questions!"}


@router.get("/{id}")
def read_item(id: str):
    table = dynamodb.Table(table_name)
    response = table.query(KeyConditionExpression=Key('id').eq(id))
    logger.info(f'response->{response}')

    return {
        'statusCode': 200,
        'headers': {},
        'body': json.dumps(response['Items'])
    }


@router.delete("/{id}")
def delete_item(id: str):
    table = dynamodb.Table(table_name)
    # response = table.query(KeyConditionExpression=Key('id').eq(id))
    response = table.delete_item(Key={'id': id})

    logger.info(f'response->{response}')

    return response
    # return {
    #     'statusCode': 200,
    #     'headers': {},
    #     'body': json.dumps(response['Items'])
    # }


@router.post("/")
def create_item(item: Question):
    table = dynamodb.Table(table_name)
    response = table.put_item(TableName=table_name, Item=item.dict())

    logger.info(f'response->{response}')

    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps({
            'message': 'Item Created',
            'id': item.id})
    }


@router.post("/search/contains")
def search_items(question: Question):
    
    table = dynamodb.Table(table_name)
    filter_conditions = []

    if question:
        for i_prop_name, i_prop_value in question.dict().items():            
            if i_prop_value is not None:
                if i_prop_name == 'id':
                    logger.info(f'm01.field.id')
                    logger.info(f'm01.field.i_prop_name=>{i_prop_name}|m01.field.i_prop_value=>{i_prop_value}')
                    filter_conditions.append(Key(i_prop_name).begins_with(i_prop_value))
                elif i_prop_name == 'answers':
                    logger.info(f'm01.field.answers')
                #     for j_answer in i_prop_value:
                #         answer_conditions = []
                #         if j_answer.is_correct is not None:
                #             answer_conditions.append(Attr('is_correct').eq(j_answer.is_correct))
                #         if j_answer.answer_text is not None:
                #             answer_conditions.append(Attr('answer_text').eq(j_answer.answer_text))
                        
                #         # Add a condition for this answer_text using OR operator
                #         filter_conditions.append(Attr('answers').contains(Attr().or_(*answer_conditions)))
                elif i_prop_name == 'question_type':
                    logger.info(f'm01.field.question_type')
                    filter_conditions.append(Attr(i_prop_name).eq(i_prop_value))
                else:
                    #filter_conditions.append(Key(i_prop_name).eq(i_prop_value))
                    #filter_conditions.append(Key(i_prop_name).begins_with(i_prop_value))
                    logger.info(f'm01.field.else')
                    logger.info(f'm01.field.i_prop_name=>{i_prop_name}|m01.field.i_prop_value=>{i_prop_value}')
                    filter_conditions.append(Attr(i_prop_name).begins_with(i_prop_value))
                    

    if filter_conditions:
        response = table.scan(FilterExpression=reduce(lambda x, y: x & y, filter_conditions))
    else:
        # No filters provided, retrieve all items
        response = table.scan()
    return response
