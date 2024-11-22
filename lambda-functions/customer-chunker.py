from pydantic.v1.utils import deep_update
import PyPDF2
#from PyPDF2 import PdfFileReader
import json
from abc import abstractmethod, ABC
from typing import List
from urllib.parse import urlparse
import boto3
import logging
from io import BytesIO
from botocore.config import Config
import os
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
#logger.setLevel(logging.INFO)

config = Config(
   retries = {
      'max_attempts': 50,
      'mode': 'standard'
   }
)

class Chunker(ABC):
    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        raise NotImplementedError()
        
class SimpleChunker(Chunker):
    def chunk(self, text: str) -> List[str]:
        words = text.split()
        return [' '.join(words[i:i+100]) for i in range(0, len(words), 100)]

prompt_template="""
Human: {prompt}

Assistant:"""

def invoke_model(prompt, client):
    query=prompt_template.format(prompt=prompt)
    request = { 
           "prompt": query,
            "max_tokens_to_sample": 150,
            "temperature": 0.1,
            "top_k": 25,
            "top_p": 0.9,
            "stop_sequences": ["\\n\\nHuman:"],
            "anthropic_version": "bedrock-2023-05-31"
            }
    response = client.invoke_model(
        body=json.dumps(request),
        #modelId="anthropic.claude-v2"
        modelId="anthropic.claude-instant-v1"
    )
    result = json.loads(response['body'].read().decode())
    return result['completion']

def lambda_handler(event, context):
    logger.info('## INPUT')
    logger.info(event)
    s3 = boto3.client('s3')
    comprehend = boto3.client('comprehend', config=config)
    bedrock = boto3.client('bedrock-runtime', config=config)

    # Extract relevant information from the input event
    input_files = event.get('inputFiles')
    input_bucket =  event.get('bucketName')

    
    if not all([input_files, input_bucket]):
        raise ValueError("Missing required input parameters")
    
    output_files = []
    chunker = SimpleChunker()

    for input_file in input_files:
        content_batches = input_file.get('contentBatches', [])
        file_metadata = input_file.get('fileMetadata', {})
        original_file_location = input_file.get('originalFileLocation', {})
        original_file_uri = original_file_location.get('s3_location', {}).get('uri', '')
        original_file_bucket_name , original_file_key = original_file_uri.replace("s3://", "").split("/", 1)
        original_file_content = read_pdf_file(s3, original_file_bucket_name, original_file_key)

        logger.info('## S3 ORIGINAL LOCATION')
        logger.info(original_file_bucket_name)
        logger.info(original_file_key)
        logger.info(original_file_content)
        
        #first_50 = os.linesep.join(original_file_content.split(os.linesep)[:50])
        #last_50 = os.linesep.join(original_file_content.split(os.linesep)[-50:])
        #logger.info('## FIRST 50')  
        #logger.info(first_50)  
        
        meta = comprehend.detect_entities(
            Text=original_file_content,
            LanguageCode='en'
        )

        entities = meta["Entities"]
        entities2 = filter(  lambda x: ( str(x["Type"]) != "OTHER" )  , entities)
        entities3 = filter(  lambda x: float(x["Score"]) > 0.5 , entities2)
        emap = {}
        for key in entities3:
            emap[key["Type"].lower()] = list(map(lambda x: x, set( [] + emap.get(key["Type"].lower(), []) + [ key["Text"].lower().strip().replace('\n','').replace(',','') ] )))

        logger.info('## COMPREHEND')           
        logger.info(emap)
        
        doc_title = invoke_model("What are the MEETING NUMBER, SESSION NUMBER, COMMITTEE NUMBER and ONE SENTENCE SUMMARY corresponding to this general assembly repport ? \n<DOCUMENT_METADATA>\n" + str(emap.get("quantity",[])) + "\n<\DOCUMENT_METADATA>\n\n<DOCUMENT>\n" + original_file_content + """\n<\DOCUMENT>\nAnswer with this JSON format:\n{"meeting_number": "<MEETING NUMBER>", "session_number":"<SESSION NUMBER>", "commitee_number":"<COMMITTEE NUMBER>", "one_sentence_summary":"<ONE SENTENCE SUMMARY>"}""",bedrock)
        logger.info('## BEDROCK TITLE')        
        logger.info(doc_title)
        


        processed_batches = []
        
        for batch in content_batches:
            input_key = batch.get('key')

            if not input_key:
                raise ValueError("Missing uri in content batch")
            
            # Read file from S3
            file_content = read_s3_file(s3, input_bucket, input_key)
            logger.info('## S3 IN BODY')
            logger.info(file_content)
            
            # Process content (chunking)
            chunked_content = process_content(file_content, chunker, doc_title)
            
            output_key = f"Output/{input_key}"
            
            # Write processed content back to S3
            logger.info('## S3 OUT')
            logger.info(chunked_content)
            
            write_to_s3(s3, input_bucket, output_key, chunked_content)
            
            # Add processed batch information
            processed_batches.append({
                'key': output_key
            })
        
        # Prepare output file information
        output_file = {
            'originalFileLocation': original_file_location,
            'fileMetadata': file_metadata,
            'contentBatches': processed_batches
        }
        output_files.append(output_file)
    
    result = {'outputFiles': output_files}
    logger.info('## RESULT')
    logger.info(result)
    
    return result
    

def read_s3_file(s3_client, bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    logger.info('## S3 IN')
    logger.info(response)
    return json.loads(response['Body'].read().decode('utf-8'))
    
def read_pdf_file(s3_client, bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    logger.info('## PDF IN')
    logger.info(response)
    pdfFileObj = response.get("Body").read()
    pdfReader = PyPDF2.PdfReader(BytesIO(pdfFileObj))
    meta = pdfReader.metadata
    logger.info(meta)
    pageObj = pdfReader.pages[0]
    page_content = pageObj.extract_text(0).strip()
    return str(page_content)

def write_to_s3(s3_client, bucket, key, content):
    s3_client.put_object(Bucket=bucket, Key=key, Body=json.dumps(content))    

def process_content(file_content: dict, chunker: Chunker, doc_title: str) -> dict:
    chunked_content = {
        'fileContents': []
    }
    
    for content in file_content.get('fileContents', []):
        content_body = content.get('contentBody', '')
        content_type = content.get('contentType', '')
        content_metadata = content.get('contentMetadata', {})
        
        words = content['contentBody']
        # chunks = chunker.chunk(words)
        chunks = [doc_title + '\n' + str(words)]
        
        for chunk in chunks:
            chunked_content['fileContents'].append({
                'contentType': content_type,
                'contentMetadata': content_metadata,
                'contentBody': chunk
            })
    
    return chunked_content