# REST endpoints that correspond to each GET and POST. Detailed, step-by-step guide on how to set this up in API Gateway:

1. Create a new REST API in API Gateway:
   - Go to [API Gateway](https://console.aws.amazon.com/apigateway?p=pm&c=sm&z=1) in the AWS Management Console
   - Choose **REST API** and click **Build**
   - Select **New API** and fill in the details:
      - API name: *DocumentProcessingAPI*
      - Description: *REST API for document processing and UI translation*
      - API Endpoint type: **Regional**
   - Click **Create API**

2. Set up resources and methods:
   - Create the **/fetch-response** resource:
      - Select the root resource ("/").
      - Click **Create Resource** button above the root resouce
      - Resource Name: **fetch-response**
      - Enable API Gateway **CORS**
      - Click **Create Resource**.

3. Create a **POST** method for **/fetch-response**:
   - With **/fetch-response**, click **Create Method**.
   - Select **POST** from the dropdown.
   - Click the checkmark to confirm.
   - Integration type: **Lambda Function**
   - Enable **Lambda Proxy integration**
   - Lambda Region: *Select your region*
   - Under Lambda Function: select the arn of the lambda function (*agent*)
   - Click **Create method**.

4. Create the **/agent-fetch-response** resource:
   *Follow the same steps as section 2, but use **agent-fetch-response** as the resource name*
   - Create **POST** method for **/agent-fetch-response**:
   *Follow the same steps as section 3, but use **agent** for the Lambda function*

5. Create the **/translate-ui-content** resource:
   *Follow the same steps as section 2, but use **translate-ui-content** as the resource name*
   - Create **POST** method for **/translate-ui-content**:
   *Follow the same steps as section 3, but use **uiTranslator** for the Lambda function*


6. Configure **request** and **response** models:
   For each method, you'll need to set up request and response models:
======================================

  ### What is a model for?
  1. **Request Validation**:
   - The request model, as defined in the JSON schema you provide, is used to validate the incoming request body.
   - When a client sends a request to the API Gateway endpoint, the request body is validated against the defined model.
   - If the request body is valid (i.e., it matches the schema), it is passed to the backend integration (in your case, the Lambda function).
   - If the request body is invalid, API Gateway will return a `400 Bad Request` response with an appropriate error message.

2. **Data Transformation**:
   - The request model can also be used to transform the incoming request body before passing it to the backend integration.
   - For example, you can map the properties in the request body to the input parameters expected by your Lambda function.

3. **Documentation and Developer Experience**:
   - By defining a request model, you can provide clear documentation and examples for clients on how to interact with your API.
   - The model information can be displayed in the API Gateway console, as well as in generated SDK and documentation.
   - This helps improve the overall developer experience and makes it easier for clients to understand and use your API.

In the case of your Lambda function, the primary benefit of using a request model is to ensure that the input data (the `prompt` in this case) is consistent and meets the expected format. This can help improve the reliability and maintainability of your application, as it reduces the chances of invalid input being passed to your Lambda function.

======================================
## Now we are going create method request and response models for resources

### 7. Starting with /fetch-response
   
   - Let us create a model for the **Method request**
      - Under **API:your-api-name**, click **Models**
      - Click **Create a model**.
      - Give the model a name, for example `FetchResponseRequest`.
      - Under **Content type**, add **application/json**.
      - Under **Model schema** add the following JSON schema
        ```json
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "title": "FetchResponseRequest",
          "type": "object",
          "properties": {
            "prompt": { "type": "string" }
          },
          "required": ["prompt"]
        }
        ```

   - Let us now create a model for the **Method response**
      - Under **API:your-api-name**, click **Models**
      - Click **Create a model**.
      - Give the model a name, for example `FetchResponseResponse`.
      - Under **Content type**, add **application/json**.
      - Under **Model schema** add the following JSON schema
        ```json
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "title": "FetchResponseResponse",
          "type": "object",
          "properties": {
            "generatedText": { "type": "string" },
            "sourceInfo": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "source": { "type": "string" },
                  "fileKey": { "type": "string" }
                }
              }
            },
            "isRTL": { "type": "boolean" }
          }
        }
     ```

## 8. Models for /agent-fetch-response
   - Let us create a model for the **Method request**
      - Under **API:your-api-name**, click **Models**
      - Click **Create a model**.
      - Give the model a name, for example `FetchAgentResponseRequest`.
      - Under **Content type**, add **application/json**.
      - Under **Model schema** add the following JSON schema
        ```json
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "title": "FetchAgentResponseRequest",
          "type": "object",
          "properties": {
            "prompt": { "type": "string" }
          },
          "required": ["prompt"]
        }
        ```

   - Let us now create a model for the **Method response**
      - Under **API:your-api-name**, click **Models**
      - Click **Create a model**.
      - Give the model a name, for example `FetchAgentResponseResponse`.
      - Under **Content type**, add `application/json`.
      - Under **Model schema** add the following JSON schema
        ```json
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "title": "FetchAgentResponseResponse",
          "type": "object",
          "properties": {
            "completion": {
              "type": "string"
            },
            "traces": {
              "type": "array",
              "items": {
                "type": "object",
                "properties": {
                  "message": {
                    "type": "string"
                  }
                }
              }
            },
            "source": {
              "type": "string"
            }
          },
          "required": ["completion", "traces", "source"]
        }
        ```

## 9. Models for /translate-ui-content
   - Let us create a model for the **Method request**
      - Under **API:your-api-name**, click **Models**
      - Click **Create a model**.
      - Give the model a name, for example `FetchUITranslatorResponseRequest`.
      - Under **Content type**, add `application/json`.
      - Under **Model schema** add the following JSON schema
        ```json
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "title": "FetchUITranslatorResponseRequest",
          "type": "object",
          "properties": {
            "sourceLanguage": {
              "type": "string"
            },
            "targetLanguage": {
              "type": "string"
            },
            "content": {
              "type": "object",
              "properties": {
                "text": {
                  "type": "string"
                }
              },
              "required": ["text"]
            }
          },
          "required": ["sourceLanguage", "targetLanguage", "content"]
        }
        ```

   - Let us now create a model for the **Method response**
      - Under **API:your-api-name**, click **Models**
      - Click **Create a model**.
      - Give the model a name, for example `FetchUITranslatorResponseResponse`.
      - Under **Content type**, add `application/json`.
      - Under **Model schema** add the following JSON schema
        ```json
        {
          "$schema": "http://json-schema.org/draft-04/schema#",
          "title": "FetchUITranslatorResponseResponse",
          "type": "object",
          "properties": {
            "translatedContent": {
              "type": "object",
              "properties": {
                "text": {
                  "type": "string"
                }
              }
            },
            "isRTL": {
              "type": "boolean"
            }
          },
          "required": ["translatedContent", "isRTL"]
        }
        ```

10. Now we can add the model to the **POST** method for **/fetch-response**
   - Click on the **POST** method under the **/fetch-response** resource
   - Select **Method request** and click **Edit**
   - Scroll down to **Request body** and expand it
   - Make sure **Content type** is set to **application/json**
   - Under **Model** select ``FetchResponseRequest`` and click **Save**
   - Now select **Method response** and click **Edit**
   - Scroll down to **Request body** and expand it
   - Again, make sure **Content type** is set to **application/json**
   - Under **Model** select **FetchResponseResponse** and click **Save**

11. Now we can add the model to the **POST** method for **/agent-fetch-response**
   - Click on the **POST** method under the **/agent-fetch-response** resource
   - Select **Method request** and click **Edit**
   - Scroll down to **Request body** and expand it
   - Make sure **Content type** is set to `application/json``     
   - Under **Model** select `FetchAgentResponseRequest` and click **Save**
   - Now select **Method response** and click **Edit**
   - Scroll down to **Request body** and expand it
   - Again, make sure **Content type** is set to **application/json**
   - Under **Model** select `FetchAgentResponseResponse` and click **Save**

11. Now we can add the model to the **POST** method for **/translate-ui-content**
   - Click on the **POST** method under the **/translate-ui-content** resource
   - Select **Method request** and click **Edit**
   - Scroll down to **Request body** and expand it
   - Make sure **Content type** is set to `application/json``     
   - Under **Model** select `TranslationRequest` and click **Save**
   - Now select **Method response** and click **Edit**
   - Scroll down to **Request body** and expand it
   - Again, make sure **Content type** is set to `application/json`
   - Under **Model** select `TranslationResponse` and click **Save*

Let us test the lambda functions
 ### no-agent.py
   - Under the **/fetch-response** **POST** method selected, select **Test**
   - Under **Request body**, let us pass a prompt to get a response. Add the following:
      ```json
      {
         "prompt": "Who is Antonio Guterres?"
      }
      ```
   - Click **Test**
   - You should be able to see a response now about Antonio Guterres

### agent.py
   - Under the **/agent-fetch-response** **POST** method selected, select **Test**
   - Under **Request body**, let us pass a prompt to get a response. Add the following:
      ```json
      {
         "prompt": "Who is Antonio Guterres?"
      }
      ```
   - Click **Test**
   - You should be able to see a response now about Antonio Guterres

### uiTranslator.py
   - Under the **/translate-ui-content** **POST** method selected, select **Test**
   - Under **Request body**, let us pass the content to be translated to get a response. Add the following:      
      ```json
      {
        "sourceLanguage": "en",
        "targetLanguage": "es",
        "content": {
          "text": "Hello, how are you?"
        }
      }
      ```
   - Click **Test**
   - You should be able to see your translated content

11. Deploy the API:
   - Click **Depploy API**.
   - Under **Stage**, select an existing stage or **New stage**
   - If **New stage** is selected, then give the stage a name, for example `Dev`. You can always create a stage before deployment by clicking on **Stages** under **Resources** in the sidebar. 
   - Even though it is optional, it is always good to give your stage a description
   - Click **Deploy**
   - You will be provided with an **Invoke URL** which can find under **Stages** in the sidebar. 
   
