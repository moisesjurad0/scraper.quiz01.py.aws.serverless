"""Principal Module."""
import logging
import os
import boto3

logger = logging.getLogger(os.environ.get('APP_NAME'))
logger.setLevel(logging.INFO)
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('API_TABLE_PYSICAL_ID')
