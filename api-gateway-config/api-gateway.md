### To transform this GraphQL schema for use with API Gateway, we'll create REST endpoints that correspond to each query and mutation. Here's a detailed, step-by-step guide on how to set this up in API Gateway:

1. Create a new REST API in API Gateway:
   a. Go to AWS Management Console > [API Gateway](https://console.aws.amazon.com/apigateway?p=pm&c=sm&z=1)
   b. Choose **REST API** and click **Build**
   c. Select **New API** and fill in the details:
      - API name: "DocumentProcessingAPI"
      - Description: "REST API for document processing and UI translation"
   d. Click "Create API"

2. Set up the **/fetch-response** endpoint:
   a. In the left sidebar, click **Resources**
   b. Click "Actions" > "Create Resource"
   c. Resource Name: "fetch-response"
   d. Resource Path: "/fetch-response"
   e. Click "Create Resource"
   f. With the new resource selected, click "Actions" > "Create Method"
   g. Choose "POST" from the dropdown and click the checkmark
   h. Set up the integration:
      - Integration type: **Lambda Function**
      - Use Lambda Proxy integration: **Check this box**
      - Lambda Function: **no-agent**
      - Click "Save"
   i. Click on **Method Request** and set up:
      - API Key Required: **true**
      - Request Validator: **Validate body**
      - Request body: **application/json**
      - Model schema:
        ```
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "type": "object",
          "properties": {
            "prompt": {"type": "string"}
          },
          "required": ["prompt"]
        }
        ```
   j. Click on "Integration Response" and set up:
      - Content type: application/json
      - Model schema:
        ```json
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "type": "object",
          "properties": {
            "generatedText": {"type": "string"},
            "sourceInfo": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "source": {"type": "string"},
                  "fileKey": {"type": "string"}
                },
                "required": ["source", "fileKey"]
              }
            },
            "isRTL": {"type": "boolean"}
          }
        }
        ```

3. Set up the /agent-fetch-response endpoint:
   Follow the same steps as for "/fetch-response", but:
   a. Resource Name: "agent-fetch-response"
   b. Resource Path: "/agent-fetch-response"
   c. Lambda Function: agent-test
   d. Use the following response model:
     ```json
     {
       "$schema": "http://json-schema.org/draft-04/schema#",
       "type": "object",
       "properties": {
         "completion": {"type": "string"},
         "traces": {
           "type": "array",
           "items": {
             "type": "object",
             "properties": {
               "agentAliasId": {"type": "string"},
               "agentId": {"type": "string"},
               "agentVersion": {"type": "string"},
               "sessionId": {"type": "string"},
               "trace": {"type": "object"}
             }
           }
         },
         "isRTL": {"type": "boolean"}
       }
     }
     ```

4. Set up the /translate-ui-content endpoint:
   a. Create a new resource named "translate-ui-content"
   b. Add a POST method and integrate with the "uiTranslator" Lambda function
   c. Set up the request model:
     ```json
     {
       "$schema": "http://json-schema.org/draft-04/schema#",
       "type": "object",
       "properties": {
         "sourceLanguage": {"type": "string"},
         "targetLanguage": {"type": "string"},
         "content": {
           "type": "object",
           "properties": {
             "buttonLabels": {"$ref": "#/definitions/ButtonLabelsInput"},
             "messages": {"$ref": "#/definitions/MessagesInput"},
             "information": {"$ref": "#/definitions/InformationInput"},
             "sideNavigation": {"$ref": "#/definitions/SideNavigationInput"},
             "languages": {"$ref": "#/definitions/LanguagesInput"},
             "header": {"$ref": "#/definitions/HeaderInput"},
             "dynamicMessages": {"$ref": "#/definitions/DynamicMessagesInput"}
           }
         }
       },
       "required": ["sourceLanguage", "targetLanguage", "content"],
       "definitions": {
         "ButtonLabelsInput": {
           "type": "object",
           "properties": {
             "submit": {"type": "string"},
             "reset": {"type": "string"},
             "getStarted": {"type": "string"},
             "learnMore": {"type": "string"},
             "learnMoreAbout": {"type": "string"}
           }
         },
         "MessagesInput": {
           "type": "object",
           "properties": {
             "loading": {"type": "string"},
             "noResponse": {"type": "string"},
             "userInputBoxPlaceHolder": {"type": "string"},
             "userInputRequired": {"type": "string"},
             "chatHeader": {"type": "string"},
             "chatModel": {"type": "string"},
             "analyzeResponse": {"type": "string"},
             "responseInsights": {"type": "string"},
             "sources": {"type": "string"},
             "dynamicMessages": {"$ref": "#/definitions/SummaryInput"}
           }
         },
         "InformationInput": {
           "type": "object",
           "properties": {
             "overviewHeader": {"type": "string"},
             "definitionsHeader": {"type": "string"},
             "benefitsHeader": {"type": "string"},
             "overview": {"type": "string"},
             "definitions": {"$ref": "#/definitions/DefinitionsInput"},
             "benefits": {"$ref": "#/definitions/BenefitsInput"},
             "languages": {"$ref": "#/definitions/LanguagesInput"}
           }
         },
         "DefinitionsInput": {
           "type": "object",
           "properties": {
             "rag": {"type": "string"},
             "langChain": {"type": "string"},
             "knowledgeBase": {"type": "string"},
             "embeddingModel": {"type": "string"}
           }
         },
         "BenefitsInput": {
           "type": "object",
           "properties": {
             "one": {"type": "string"},
             "two": {"type": "string"}
           }
         },
         "LanguagesInput": {
           "type": "object",
           "properties": {
             "Arabic": {"type": "string"},
             "Chinese": {"type": "string"},
             "English": {"type": "string"},
             "French": {"type": "string"},
             "Russian": {"type": "string"},
             "Spanish": {"type": "string"}
           }
         },
         "HeaderInput": {
           "type": "object",
           "properties": {
             "demo": {"type": "string"},
             "preparedBy": {"type": "string"}
           }
         },
         "SideNavigationInput": {
           "type": "object",
           "properties": {
             "header": {"type": "string"},
             "home": {"type": "string"},
             "actions": {"type": "string"},
             "naiveRAG": {"type": "string"},
             "agentRAG": {"type": "string"},
             "signOut": {"type": "string"},
             "loggedInAs": {"type": "string"}
           }
         },
         "DynamicMessagesInput": {
           "type": "object",
           "properties": {
             "summary": {"$ref": "#/definitions/SummaryInput
