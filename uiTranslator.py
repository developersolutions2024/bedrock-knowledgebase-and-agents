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
        
def lambda_handler(event, context):
    # Log the entire event to ensure we are receiving the correct structure
    print("Event received from AppSync:", event)
   
    # Extract the arguments from the AppSync event
    source_language = event.get('arguments', {}).get('sourceLanguage', '')
    target_language = event.get('arguments', {}).get('targetLanguage', '')
    content = event.get('arguments', {}).get('content', {})
    
    is_rtl = True if target_language == 'ar' else False
    
    def translate_text(text):
        result = translate.translate_text(
            Text=text,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        return result.get('TranslatedText')

    # Recursively translate the content
    def recursive_translate(obj):
        if isinstance(obj, dict):
            return {key: recursive_translate(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [recursive_translate(item) for item in obj]
        elif isinstance(obj, str):
            return translate_text(obj)
        else:
            return obj

    translated_content = recursive_translate(content)
    # detected_language = detect_language(translated_content)
    # print("Detected Language: ", detected_language)
    
     
    print("Is Arabic? ", is_rtl)

    print("Translated Content:", translated_content)
   
    return translated_content



