import logging
import os
import boto3

logger = logging.getLogger('exam02-api')
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('API_TABLE')
