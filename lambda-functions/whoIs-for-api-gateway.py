import boto3
import json
import random
import string
from botocore.config import Config

AGENT_ID = 'agent-id'
AGENT_ALIAS_ID = 'agent-alias-id'

SESSION_ID_LENGTH = 10

config = Config(
   connect_timeout = 5,
   read_timeout = 600,
   retries = {
      'max_attempts': 50,
      'mode': 'standard'
   }
)

def process_response(response):
    print('\nprocess_response', response)

    completion = ''
    trace_array = []  
    return_control_invocation_results = []

    # New: Extract and print the source information from the sessionState if present
    source_info = "Unknown Source"  # Default value if not found
    if 'sessionState' in response and 'files' in response['sessionState']:
        files = response['sessionState']['files']
        for file in files:
            if 'source' in file and 's3Location' in file['source']:
                source_info = file['source']['s3Location'].get('uri', 'Unknown source')
                print(f"S3 Source URI: {source_info}")

    # Print the source info to CloudWatch
    print(f"Source: {source_info}")

    for event in response.get('completion', []):

        if 'returnControl' in event:
            return_control = event['returnControl']
            print('\n- returnControl', return_control)
            invocation_id = return_control['invocationId']
            invocation_inputs = return_control['invocationInputs']

            for invocation_input in invocation_inputs:
                function_invocation_input = invocation_input['functionInvocationInput']
                action_group = function_invocation_input['actionGroup']
                function = function_invocation_input['function']
                parameters = function_invocation_input['parameters']
                if action_group == 'retrieve-customer-settings' and function == 'retrieve-customer-settings-from-crm':
                    return_control_invocation_results.append({
                        'functionResult': {
                            'actionGroup': action_group,
                            'function': function,
                            'responseBody': {
                                'TEXT': {
                                    'body': '{ "customer id": 12345 }'  # Simulated API
                                }
                            }
                        }
                    })

        elif 'chunk' in event:
            chunk = event["chunk"]
            print('\n- chunk', chunk)
            completion += chunk["bytes"].decode()

        elif 'trace' in event:
            trace = event["trace"]
            trace_array.append(trace)
            print('\n- trace', trace)

        else:
            print('\nevent', event)

    if len(completion) > 0:
        print('\ncompletion\n')
        print(completion)

    if len(return_control_invocation_results) > 0:
        print('\n- returnControlInvocationResults', return_control_invocation_results)
        new_response = bedrock_agent_runtime.invoke_agent(
            enableTrace=True,
            agentId=AGENT_ID,
            agentAliasId=AGENT_ALIAS_ID,
            sessionId=session_id,
            sessionState={
                'invocationId': invocation_id,
                'returnControlInvocationResults': return_control_invocation_results
            },
        )
        process_response(new_response)

    return {
        "completion": completion,
        "traces": trace_array,
        "source": source_info  # Include the source in the returned object
    }

# MAIN

bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name='us-east-1', config=config)

def lambda_handler(event, context):
    print('Event:', event)

    # Extract the input data from the API Gateway event
    try:
        body = json.loads(event['body'])
        user_input = body.get('prompt', '')
    except (KeyError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request body'})
        }

    system_prompt = (
       "Always respond accurately in the same language the user is writing"
    )
    full_prompt = f"{system_prompt}\n\nQuestion: {user_input}\nAnswer:"
    input_text = full_prompt

    print('\ninputText')
    print(input_text)

    session_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=SESSION_ID_LENGTH))
    print('sessionId', session_id)

    # Add a source to the sessionState
    session_attributes = {
        'sessionAttributes': {
            'source': 'User Query: Document Analysis'  # Example source value
        }
    }

    # Call the invoke_agent API with the sessionState and source
    first_response = bedrock_agent_runtime.invoke_agent(
        enableTrace=True,
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=input_text,
        sessionState=session_attributes  # Pass the session attributes with the source
    )

    answer = process_response(first_response)

    # Prepare the response
    response_body = {
        'completion': answer['completion'],
        'traces': answer['traces'],
        'source': answer['source']
    }

    # Return the response in the format expected by API Gateway
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Adjust this for your CORS policy
        },
        'body': json.dumps(response_body)
    }
