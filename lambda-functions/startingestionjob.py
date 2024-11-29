import boto3
import json
from datetime import datetime

client = boto3.client('bedrock-agent')

def lambda_handler(event, context):
    try:
        response = client.start_ingestion_job(
            knowledgeBaseId='your-knowledgebase-id',
            dataSourceId='your-datasource-id'
        )
        
        # Manually convert any datetime objects to string in the response
        def convert_datetime(item):
            if isinstance(item, dict):
                for key, value in item.items():
                    item[key] = convert_datetime(value)
            elif isinstance(item, list):
                return [convert_datetime(i) for i in item]
            elif isinstance(item, datetime):
                return item.isoformat()
            return item
        
        # Convert datetime objects in the response
        response_converted = convert_datetime(response)
        
        # Returns the response as an object
        return {
            'statusCode': 200,
            'body': response_converted
        }
    except Exception as e:
        return{
            'statusCode': 200,
            'body': str(e)
        }
