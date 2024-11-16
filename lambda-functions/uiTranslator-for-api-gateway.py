import json
import boto3

comprehend_client = boto3.client('comprehend')
translate = boto3.client('translate')

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

def translate_text(text, source_language, target_language):
    result = translate.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language
    )
    return result.get('TranslatedText')

def recursive_translate(obj, source_language, target_language):
    if isinstance(obj, dict):
        return {key: recursive_translate(value, source_language, target_language) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [recursive_translate(item, source_language, target_language) for item in obj]
    elif isinstance(obj, str):
        # Check if the source language is RTL
        if source_language == 'ar':
            # Wrap the text in Unicode control characters to preserve RTL formatting
            return u'\u202b' + translate_text(obj, source_language, target_language) + u'\u202c'
        else:
            return translate_text(obj, source_language, target_language)
    else:
        return obj

def lambda_handler(event, context):
    print('Event:', event)

    # Extract the input data from the API Gateway event
    try:
        body = json.loads(event['body'])
        source_language = body.get('sourceLanguage', '')
        target_language = body.get('targetLanguage', '')
        content = body.get('content', {})
    except (KeyError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request body'})
        }

    is_rtl = True if target_language == 'ar' else False

    translated_content = recursive_translate(content, source_language, target_language)
    detected_language = detect_language(json.dumps(translated_content))
    print("Detected Language: ", detected_language)
    print("Is Arabic? ", is_rtl)
    print("Translated Content:", translated_content)

    # Prepare the response
    response_body = {
        'translatedContent': translated_content,
        'isRTL': is_rtl
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
