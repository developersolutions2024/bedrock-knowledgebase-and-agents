import sys
import json
import boto3
import re
import json
import PyPDF2
import logging
import datetime
import pip._internal as pip
from io import BytesIO
from botocore.config import Config
from urllib.parse import urlparse
from langchain_aws import ChatBedrock


config = Config(
   connect_timeout = 5,
   read_timeout = 600,
   retries = {
      'max_attempts': 50,
      'mode': 'standard'
   }
)

kb_id = os.environ.get('KNOWLEDGE_BASE_ID', '')
log_level = os.environ.get('LOG_LEVEL', 'ERROR').upper()
aws_region = os.environ.get('AWS_REGION', 'us-east-1')

logger = logging.getLogger()
logger.setLevel(log_level)
# logger.setLevel(logging.INFO)


bedrock_client = boto3.client(
    'bedrock-agent-runtime',
    region_name = aws_region,
    config=config
)

s3 = boto3.client(
    's3',
    config=config,
    region_name = aws_region
)

def lambda_handler(event, context):
    tokenLimit = 5
    limit = 1000

    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])

    meeting_number = int(next((item for item in parameters if item["name"] == "meeting_number"), 0)["value"])
    session_number = int(next((item for item in parameters if item["name"] == "session_number"), 0)["value"])
    logger.info("## MEETING NUMBER")
    logger.info(str(meeting_number))
    logger.info("## SESSION NUMBER")
    logger.info(str(session_number))

    one_group_filter = {
        "andAll": [
            {
                "equals": {
                    "key": "meeting_number",
                    "value": meeting_number
                }
            },
            {
                "equals": {
                    "key": "session_number",
                    "value": session_number
                }
            }
        ]
    }

    prompt = "write a one sentence summary of the " + str(meeting_number) + " th meeting from the " + str(session_number) + " th session" 

    response = bedrock_client.retrieve_and_generate(
        input={
            'text': prompt
        },
        retrieveAndGenerateConfiguration = {
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': kb_id,  # Ensure this ID is correct for your knowledge base
                'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0',
                'retrievalConfiguration': {
                    'vectorSearchConfiguration': {
                        'overrideSearchType': 'HYBRID',
                        'numberOfResults': 1,
                        'filter': one_group_filter
                    }
                }
            },
            'type': 'KNOWLEDGE_BASE'
        }
    )


    # Extract the generated output text
    output_text = response.get('output', {}).get('text', '')
    
    # Initialize a list to hold the source information
    source_info = []
    
    # Extract the source URIs from the citations
    citations = response.get('citations', [])

    short_summary = ""
    if citations:
        for citation in citations:
            for reference in citation.get('retrievedReferences', []):
                # Get the URI from the S3 location
                uri = reference.get('location', {}).get('s3Location', {}).get('uri', '')
                if uri:
                    # Clean the 's3://' prefix
                    clean_uri = uri.replace('s3://', '')
                   
                    # Generate a pre-signed URL for the source
                    content = reference.get('content', {}).get('text', '')
                    short_summary = content
                    metadata = reference.get('metadata', {})
                    parsed_uri = urlparse(uri)
                    bucket_name = parsed_uri.netloc
                    object_key = parsed_uri.path.lstrip('/')
                   
                    try:
                        presigned_url = s3.generate_presigned_url(
                            'get_object',
                            Params={
                                'Bucket': bucket_name,
                                'Key': object_key
                            },
                            ExpiresIn=10800  # URL expires in 3 hours
                        )
                        source_info.append({
                            'source': presigned_url,
                            'bucket': bucket_name,
                            'fileKey': object_key,
                            'content': content,
                            'metadata': metadata
                        })
                    except Exception as e:
                        source_info.append({
                            'source': clean_uri,
                            'fileKey': object_key,
                            'content': content,
                            'metadata': metadata
                        })

    if len(source_info) == 0:
        response_body = {
            'TEXT': {
                'body': 'Sorry. I can not find any document about this topic'
            }
        }
        function_response = {
            'actionGroup': event['actionGroup'],
            'function': event['function'],
            'functionResponse': {
                'responseBody': response_body
            }
        }
        session_attributes = event['sessionAttributes']
        prompt_session_attributes = event['promptSessionAttributes']
        action_response = {
            'messageVersion': event['messageVersion'], 
            'response': function_response
        }
        return action_response

    body = { 
        #"generated_summary": output_text,
        "summary" : short_summary,
        "sources": source_info
    }

    response_body = {
        'TEXT': {
        #'application/json': {
            'body': json.dumps(body)
        }
    }

    function_response = {
        'actionGroup': event['actionGroup'],
        'function': event['function'],
        'functionResponse': {
            'responseBody': response_body
        }
    }

    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    prompt_session_attributes["sources"] = json.dumps(source_info)

    action_response = {
        'messageVersion': event['messageVersion'], 
        'response': function_response,
        'promptSessionAttributes': prompt_session_attributes
        #'sessionAttributes': session_attributes,
    }

    logger.info("## ANSWER")
    logger.info(str(action_response))

    return action_response


