import sys
import json
import boto3
import re
import json
import PyPDF2
from io import BytesIO
from langchain.docstore.document import Document
from langchain.llms import Bedrock
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from botocore.config import Config
import logging
import datetime
from urllib.parse import urlparse

config = Config(
   connect_timeout = 5,
   read_timeout = 300,
   retries = {
      'max_attempts': 50,
      'mode': 'standard'
   }
)

logger = logging.getLogger()
logger.setLevel(logging.ERROR)
#logger.setLevel(logging.INFO)

boto3_bedrock = boto3.client(
    'bedrock-runtime',
    region_name = 'us-east-1',
    config=config
)

bedrock_client = boto3.client(
    'bedrock-agent-runtime',
    region_name = 'us-east-1',
    config=config
)

s3_client = boto3.client('s3')


def lambda_handler(event, context):
    tokenLimit = 5
    limit = 1000
    
    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    
    
    topic = next((item for item in parameters if item["name"] == "topic"), '')["value"]
    print("TOPIC : " + str(topic))
    
    prompt = """Write a long detailled biography of """ + str(topic) + """ . Summarise the main role, events and actions related to this person in a chronology. Include date and place of birth. Mention schools, degrees and professional resume. Highlight the role and impact in the United Nations"""
 
    
    try:
        # Call Bedrock to retrieve and generate the response
        response = bedrock_client.retrieve_and_generate(
            input={
                'text': prompt
            },
            retrieveAndGenerateConfiguration= {
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': 'H7RLOFWFX6',  # Ensure this ID is correct for your knowledge base
                    'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0',
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'overrideSearchType': 'HYBRID',
                            'numberOfResults': 20
                        }
                    },
                    'generationConfiguration': {
                        'inferenceConfig': {
                            'textInferenceConfig': {
                                'maxTokens': 600
                            }
                        }
                    },
                    'orchestrationConfiguration': {
                        'queryTransformationConfiguration': {
                            'type': 'QUERY_DECOMPOSITION'
                        }
                    }
                },          
                'type': 'KNOWLEDGE_BASE'
            }
        )
    except Exception as e:
        return {
            'errorMessage': f"Error retrieving or generating response: {str(e)}"
        }
    
    # Extract the generated output text
    output_text = response.get('output', {}).get('text', '')
    
    # Initialize a list to hold the source information
    source_info = []
    
    # Extract the source URIs from the citations
    citations = response.get('citations', [])
    
    if citations:
        for citation in citations:
            for reference in citation.get('retrievedReferences', []):
                # Get the URI from the S3 location
                uri = reference.get('location', {}).get('s3Location', {}).get('uri', '')
                if uri:
                    # Clean the 's3://' prefix
                    clean_uri = uri.replace('s3://', '')
                   
                    # Generate a pre-signed URL for the source
                    parsed_uri = urlparse(uri)
                    bucket_name = parsed_uri.netloc
                    object_key = parsed_uri.path.lstrip('/')
                   
                    try:
                        presigned_url = s3_client.generate_presigned_url(
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
                            'fileKey': object_key
                        })
                    except Exception as e:
                        print(f"Error generating pre-signed URL: {str(e)}")
                        source_info.append({
                            'source': clean_uri,
                            'fileKey': object_key
                        })
    
    print(source_info)
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
        print(str(action_response))
        return action_response
                      
    
    # DOC : Agent Lambda : https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
    print(json.dumps(output_text))
    
    
    body = {
        "biography" : output_text,
        "sources": source_info
    }

    response_body = {
        'TEXT': {
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
    print(str(action_response))
        
    return action_response
    

