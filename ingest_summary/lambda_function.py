import warnings
import os
os.chdir('/tmp')

with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import sys
    import json
    import boto3
    import re
    import json
    from io import BytesIO
    from langchain.docstore.document import Document
    from langchain.llms import Bedrock
    from langchain.chains.summarize import load_summarize_chain
    from langchain.prompts import PromptTemplate
    from botocore.config import Config
    import logging
    import datetime
    from urllib.parse import urlparse
    import pip._internal as pip
    from pydantic.v1.utils import deep_update
    from abc import abstractmethod, ABC
    from typing import List
    from urllib.parse import urlparse
    import boto3
    import logging
    from io import BytesIO
    from botocore.config import Config
    from langchain_aws import ChatBedrock
    from langchain_aws import ChatBedrockConverse
    from langchain_core.rate_limiters import InMemoryRateLimiter


log_level = str(os.environ.get('LOGLEVEL', 'ERROR').upper())
#print(log_level)
logger = logging.getLogger()
logger.setLevel(log_level)

# REGION
region = os.environ.get('AWS_REGION', 'us-east-1')

# SUMMARISATION PARAMETER
tokenLimit = 5 # MINIMUM SIZE
limit = 1000 # MAXIMUM SIZE

config = Config(
   connect_timeout = 5,
   read_timeout = 600,
   retries = {
      'max_attempts': 50,
      'mode': 'standard'
   }
)


s3 = boto3.client('s3', config=config, region_name = region)
bedrock = boto3.client('bedrock-runtime', config=config, region_name = region)
# # COMPREHEND COULD BE USED TO BRING MORE CONTEXT
# comprehend = boto3.client('comprehend', config=config, region_name = region)


# INVOKE MODEL TO GET JSON METADATA

json_schema = {
  "title": "Document",
  "type": "object",
  "required": ["meeting_number", "session_number", "committee_number", "one_sentence_summary"],
  "properties": {
    "meeting_number": {
      "type": "integer",
      "default": 0,
      "description": "The meeting number."
    },      
    "committee_number": {
      "type": "integer",
      "default": 0,
      "description": "The committee number."
    },
    "session_number": {
      "type": "integer",
      "default": 0,
      "description": "The session number."
    },
    "one_sentence_summary": {
      "description": "A one sentence summary of the meeting report.",
      "type": "string",
      "default": ""
    }
  }
}


def invoke_model2(prompt, client):
    request = {
        "anthropic_version": "bedrock-2023-05-31",    
        "max_tokens": 200,
        "system": "You are a meeting report reader and you are able to provide specific information from the report in JSON format.",    
        "messages": [
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": prompt }
                ]
            }
            #,{
            #    "role": "assistant",
            #    "content": [
            #        {  "type": "text", "text": """{"meeting_number":""" }  # Prefill here
            #    ]
            #}
        ],
        "temperature": 0.1,
        "top_p": 0.9,
        "top_k": 25,
        "tools": [
            {
                "name": "metadata_extractor",
                "description": "Extract specific information about a meeting from the meeting report. Information include meeting number, session number, committee number and one sentence summary of the meeting report",
                "input_schema": json_schema
                
            }
        ],
        "tool_choice": {
            "type" :  "tool",
            "name" : "metadata_extractor",
        }
    }  

    response = client.invoke_model(
        body=json.dumps(request),
        modelId="us.anthropic.claude-3-haiku-20240307-v1:0"
    )
    result = json.loads(response['body'].read().decode())
    content = result["content"]
    tool_use = ""
    for c in content:
        if c["type"] == "tool_use":
            tool_use = c['input']
    return tool_use


rate_limiter = InMemoryRateLimiter(
    requests_per_second=1,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=1,  # Controls the maximum burst size.
)


llm3 = ChatBedrockConverse(
    model = "us.anthropic.claude-3-haiku-20240307-v1:0",
    max_tokens = 400,
    temperature = 0.01,
    top_p = 0.9,
    region_name = region,
    rate_limiter = rate_limiter,
    config = config
)


map_prompt_template = """
Human: 
Extract the most important information from the following report:
<report>
{text}
</report>

Assistant:
<result>
"""

combine_prompt_template = """
Human: 
Write bullet points to summarize the following reports :
<report>
{text}
</report>

Assistant:
<result>
"""

map_prompt_template2 = """
Extract the most important information from the following report:
<report>
{text}
</report>

"""

combine_prompt_template2 = """
Write bullet points to summarize the following reports :
<report>
{text}
</report>

"""

map_prompt = PromptTemplate(template=map_prompt_template2, input_variables=["text"])
combine_prompt = PromptTemplate(template=combine_prompt_template2, input_variables=["text"])

# DOC : migrate to Claude 3 : https://python.langchain.com/docs/integrations/chat/bedrock/
# DOC : https://api.python.langchain.com/en/latest/chains/langchain.chains.summarize.__init__.load_summarize_chain.html#langchain.chains.summarize.__init__.load_summarize_chain
# DOC return_only_output : https://api.python.langchain.com/en/latest/agents/langchain.agents.agent.AgentExecutor.html?highlight=return_intermediate_steps#langchain.agents.agent.AgentExecutor.return_intermediate_steps
summary_chain = load_summarize_chain(llm=llm3, chain_type="map_reduce", verbose=False, map_prompt=map_prompt, combine_prompt=combine_prompt, return_intermediate_steps=True )


class Chunker(ABC):
    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        raise NotImplementedError()
        
class SimpleChunker(Chunker):
    def chunk(self, text: str) -> List[str]:
        words = text.split()
        return [' '.join(words[i:i+100]) for i in range(0, len(words), 100)]


def read_s3_file(s3_client, bucket, key):
    response = s3_client.get_object(Bucket=bucket, Key=key)
    logger.info('## S3 IN')
    logger.info(response)
    return json.loads(response['Body'].read().decode('utf-8'))
    

def write_to_s3(s3_client, bucket, key, content):
    s3_client.put_object(Bucket=bucket, Key=key, Body=json.dumps(content))    

def process_content(file_content: dict, chunker: Chunker) -> dict:
    chunked_content = {
        'fileContents': []
    }
    
    for content in file_content.get('fileContents', []):
        
        content_body = content.get('contentBody', '')
        content_type = content.get('contentType', '')
        content_metadata = content.get('contentMetadata', {})
        page_content = " ".join(content_body.split()[:1000]) # first 1000 words
        
        # meta = comprehend.detect_entities(
        #     Text=page_content,
        #     LanguageCode='en'
        # )

        # entities = meta["Entities"]
        # entities2 = filter(  lambda x: ( str(x["Type"]) != "OTHER" )  , entities)
        # entities3 = filter(  lambda x: float(x["Score"]) > 0.5 , entities2)
        # emap = {}
        # for key in entities3:
        #     emap[key["Type"].lower()] = list(map(lambda x: x, set( [] + emap.get(key["Type"].lower(), []) + [ key["Text"].lower().strip().replace('\n','').replace(',','') ] )))
 
        # logger.info('## COMPREHEND')           
        # logger.info(emap)

        #doc_title = invoke_model2("\n\nHuman:\nWhat are the MEETING NUMBER, SESSION NUMBER, COMMITTEE NUMBER and ONE SENTENCE SUMMARY corresponding to this general assembly report ? \n<DOCUMENT_METADATA>\n" + str(emap.get("quantity",[])) + "\n<\DOCUMENT_METADATA>\n\n<DOCUMENT>\n" + page_content + """\n<\DOCUMENT>\nAnswer following this JSON format:\n{"meeting_number": <MEETING NUMBER>, "session_number": <SESSION NUMBER>, "committee_number": <COMMITTEE NUMBER>, "one_sentence_summary": "<ONE SENTENCE SUMMARY>"}\nUse 0 (zero) as a default fallback integer and "" (Empty string) as default fallback string if a value is missing""" + "\nAssistant:",bedrock)
        doc_title = invoke_model2("\n\nHuman:\nWhat are the MEETING NUMBER, SESSION NUMBER, COMMITTEE NUMBER and ONE SENTENCE SUMMARY corresponding to this general assembly report ?\n\n<DOCUMENT>\n" + page_content + """\n<\DOCUMENT>\nAnswer following this JSON format:\n{"meeting_number": <MEETING NUMBER>, "session_number": <SESSION NUMBER>, "committee_number": <COMMITTEE NUMBER>, "one_sentence_summary": "<ONE SENTENCE SUMMARY>"}\nUse 0 (zero) as a default fallback integer and "" (Empty string) as default fallback string if a value is missing""" + "\nAssistant:",bedrock)

        logger.info('## BEDROCK TITLE')        
        logger.info(doc_title)
        json_title = json.dumps(doc_title)
        
        docListPdf = []
        tooBig = 0

        title = str(doc_title)
        content = content_body
                                                    
        logger.info('DOC : ' + title)
        char = str( len( content ) )
        token = str( len( content.split() ) )
        #token = str( llm2.get_num_tokens(content) )
        logger.info('CHAR = ' + char + ' TOKEN = ' + token )
        # logger.info(content)
        
        # # EXTRACT INFORMATION WITH COMPREHEND ()
        # meta = comprehend.detect_entities(
        #     Text=content,
        #     LanguageCode='en'
        # )
        # entities = meta["Entities"]
        # entities1 = filter(  lambda x: ( str(x["Type"]) != "QUANTITY" ) and ( str(x["Type"]) != "OTHER" )  , entities)
        # entities2 = filter(  lambda x: float(x["Score"]) > 0.99 , entities1)
        # emap = set(map( lambda x: str(x["Type"]).lower() + " : " + str(re.sub('[^a-z0-9 ]+', ' ', x["Text"].lower())),entities2))
        # logger.info(emap)
        
        nowStart = datetime.datetime.now()
        logger.info ("Split date and time : ")
        logger.info (nowStart.strftime("%Y-%m-%d %H:%M:%S"))

        doc_list = []
        parListPdf = []

        split = content.split()
        length = len(split)
        if length > limit:
            tooBig = tooBig + 1
            # logger.info("Too big : CUT")
            # logger.info("Too big : " + sentence[0])
            sentence_split = re.split(r'(?<=\b)\.(?=[\s\n]|$)', content)
            # logger.info("###### CUT ###### ") 
            accumulator = ""
            for i in sentence_split:
                i_size = len(i.split())
                # logger.info("bloc : " + str(i_size) + " ## " + i)
                if ( len(accumulator.split()) + i_size ) < limit:
                    # logger.info("Cumul")
                    accumulator = accumulator + i + " ."
                else:
                    # logger.info("Push new bloc : " + str(len(accumulator.split())) + " ## " + accumulator)
                    doc_list.append(str(accumulator))

                    key = ' '.join(accumulator.split()[:5])
                    logger.info('#########')
                    # logger.info('DOC : ' + title)
                    char = str( len( accumulator ) )
                    token = str( len( accumulator.split() ) )
                    #token = str( llm2.get_num_tokens(accumulator) )
                   
                    if int(token) > tokenLimit:
                        logger.info('  PART : CHAR = ' + char + ' TOKEN = ' + token )
                        parListPdf.append(Document(metadata={'title':title + ' - ' + key,'char': char,'token': token},page_content=(accumulator)))

                    accumulator = ""
                    if ( len(accumulator.split()) + i_size ) < limit:
                        accumulator = accumulator + i
                    else:
                        logger.info("too big sentence")  
        else:
            sentence_split = re.split(r'(?<=\b)\.(?=[\s\n]|$)', content)
            sentence_join = ' .'.join(sentence_split)
            doc_list.append(str(sentence_join))

            key = ' '.join(sentence_join.split()[:5])
            logger.info('#########')
            # logger.info('DOC : ' + title)
            char = str( len( sentence_join ) )
            token = str( len( sentence_join.split() ) )
            #token = str( llm2.get_num_tokens(sentence_join) )
            if int(token) > tokenLimit:
                logger.info('  PART : CHAR = ' + char + ' TOKEN = ' + token )
                parListPdf.append(Document(metadata={'title':title + ' - ' + key,'char': char,'token': token},page_content=sentence_join))

        docListPdf.append(parListPdf)

        nowEnd = datetime.datetime.now()
        logger.info ("End split date and time : ")
        logger.info (nowEnd.strftime("%Y-%m-%d %H:%M:%S"))

        # logger.info METADATA 
        logger.info("Paragraph number : ")
        logger.info(len(docListPdf))
        logger.info("Paragraph metadata : ")

        # RUN THE SUMMARIZATION
        nowStart = datetime.datetime.now()
        logger.info ("Start date and time : ")
        logger.info (nowStart.strftime("%Y-%m-%d %H:%M:%S"))
        outpoutList = []
        # for doc in docListPdf[:10]:
        for doc in docListPdf:
            output = summary_chain( {"input_documents": doc},return_only_outputs=True )
            outpoutList.append(output)
        nowEnd = datetime.datetime.now()
        logger.info ("End date and time : ")
        logger.info (nowEnd.strftime("%Y-%m-%d %H:%M:%S"))

        # PROCESS RESULT
        finalDocList = []
        for docIdx,output in enumerate(outpoutList):
            logger.info( f'\n\n# DOC {docIdx} #' )
            result = output['output_text']
            finalDocList.append(Document(metadata={'title':f'doc_{docIdx}','char': 0,'token': 0},page_content=result.strip()))

        # DOC : Agent Lambda : https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html
        # print(finalDocList[0].page_content)

        # RETURN THE CHUNK. IT IS REPLACED BY THE SUMMARY INCLUDING THE EXTRA METADATA
        chunked_content['fileContents'].append({
            'contentType': content_type,
            'contentMetadata': doc_title,
            'contentBody': json_title + '\n' + str(finalDocList[0].page_content)
        })

        return chunked_content


def lambda_handler(event, context):
    logger.info('## INPUT')
    logger.info(event)

    # Extract relevant information from the input event
    input_files = event.get('inputFiles')
    input_bucket = event.get('bucketName')

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
            chunked_content = process_content(file_content, chunker)
            
            output_key = f"Output/{input_key}"
            
            # Write processed content back to S3
            logger.warning('## S3 OUT')
            logger.warning(chunked_content)
            
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
    logger.warning('## RESULT')
    logger.warning(result)

    return result
    



