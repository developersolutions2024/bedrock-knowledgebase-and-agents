import json
import boto3
from urllib.parse import urlparse

# Initialize the Bedrock client
bedrock_client = boto3.client('bedrock-agent-runtime')
s3_client = boto3.client('s3')
comprehend_client = boto3.client('comprehend')
 

def detect_language(text):
    try:
        # Detect dominant language using Comprehend
        response = comprehend_client.detect_dominant_language(Text=text)
        if 'Languages' in response and len(response['Languages']) > 0:
            dominant_language = response['Languages'][0]['LanguageCode']
            return dominant_language
        else:
            return None
    except Exception as e:
        print(f'Error detecting language: ${str(e)}')
        return None

def lambda_handler(event, context):
    print('Event:', event)
    # Extract the user prompt from the event
    prompt_event = event['arguments']
    user_prompt = prompt_event.get('prompt', '')
    modelArn = 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0'
   
    
    # Detect the language of the prompt
    detected_language = detect_language(user_prompt)
    print("Detected Language: ", detected_language)
    
    # Determine if the text is in arabic
    is_rtl = detected_language == 'ar'
    
    try:
        # Call Bedrock to retrieve and generate the response
        response = bedrock_client.retrieve_and_generate(
            input={
                'text': user_prompt
            },
            retrieveAndGenerateConfiguration= {
                'knowledgeBaseConfiguration': {
                    'generationConfiguration': {
                        'inferenceConfig': {
                          'textInferenceConfig': {
                              'maxTokens': 1000
                            }
                        }
                    },
                    'knowledgeBaseId': 'your-knowledge-base-ID',  # Ensure this ID is correct for your knowledge base
                    'modelArn': modelArn,
                    'retrievalConfiguration': {
                        'vectorSearchConfiguration': {
                            'overrideSearchType': 'HYBRID',
                            'numberOfResults': 10
                        }
                    },
                    'orchestrationConfiguration': {
                        'queryTransformationConfiguration': {
                        'type': 'QUERY_DECOMPOSITION'
                }
            },
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
                            'fileKey': object_key
                        })
                    except Exception as e:
                        print(f"Error generating pre-signed URL: {str(e)}")
                        source_info.append({
                            'source': clean_uri,
                            'fileKey': object_key
                        })
   
    # Return the generated text and the source information
    return {
        'generatedText': output_text,
        'sourceInfo': source_info if source_info else [
            {'source': '', 'fileKey': ''}
        ],
        'isRTL': is_rtl # Returns whether the text should be render RTL
         
    }
