import logging
import os
import boto3

logger = logging.getLogger('exam-api')
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('QUESTIONS_TABLE')
