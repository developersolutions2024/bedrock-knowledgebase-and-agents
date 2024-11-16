### To transform this GraphQL schema for use with API Gateway, we'll create REST endpoints that correspond to each GET and POST. Here's a detailed, step-by-step guide on how to set this up in API Gateway:

1. Create a new REST API in API Gateway:
   - Go to AWS Management Console > [API Gateway](https://console.aws.amazon.com/apigateway?p=pm&c=sm&z=1)
   - Choose **REST API** and click **Build**
   - Select **New API** and fill in the details:
      - API name: *DocumentProcessingAPI*
      - Description: *REST API for document processing and UI translation*
      - API Endpoint type: **Regional**
   - Click **Create API**

2. Set up resources and methods:
   - Create **/fetch-response** resource:
      - Select the root resource ("/").
      - Click**Create Resource** button above the root resouce
      - Resource Name: **fetch-response**
      - Enable API Gateway **CORS**
      - Click **Create Resource**.

3. Create **POST** method for **/fetch-response**:
   - With **/fetch-response**, click **Create Method**.
   - Select **POST** from the dropdown.
   - Click the checkmark to confirm.
   - Integration type: **Lambda Function**
   - Enable **Lambda Proxy integration**
   - Lambda Region: *Select your region*
   - Under Lambda Function: select the arn of the lambda function (*agent*)
   - Click **Create method**.

4. Create **/agent-fetch-response** resource:
   *Follow the same steps as section 2, but use **agent-fetch-response** as the resource name*
   - Create **POST** method for **/agent-fetch-response**:
   *Follow the same steps as section 3, but use **agent** for the Lambda function*

5. Create **/translate-ui-content** resource:
   *Follow the same steps as section 2, but use **translate-ui-content** as the resource name*
   - Create **POST** method for **/translate-ui-content**:
   *Follow the same steps as section 3, but use **uiTranslator** for the Lambda function*

6. Create **prompt-answers** resource:
   *Follow the same steps as section 2, but use **prompt-answers** as the resource name*

7. Create **GET** method for **/prompt-answers**:
   a. With "/prompt-answers" selected, choose "Actions" > "Create Method".
   b. Select "GET" from the dropdown.
   c. Click the checkmark to confirm.
   d. Integration type: Lambda Function
   e. Use Lambda Proxy integration: Yes
   f. Lambda Region: Select your region
   g. Lambda Function: (create a new Lambda function for this, e.g., "get-prompt-answers")
   h. Click "Save".
   i. When prompted to add permission to Lambda function, click "OK".

7. Configure **request** and **response** models:
   For each method, you'll need to set up request and response models:

   - Go to the method's **Method Request**.
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

   b. Under **API:your-api-name**, click **Models**
   c. Create a model for the request (if needed) in "Models" section of API Gateway.
   d. Go to the method's "Integration Request".
   e. Under "Mapping Templates", add a mapping template for "application/json".
   f. Go to the method's "Method Response".
   g. Add appropriate response models for different status codes.

   Example for "/fetch-response" POST:
   - Request model:
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
   - Response model:
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

4. Set up request validators:
   a. Go to "Models" in the API Gateway console.
   b. Create request validators for each endpoint to ensure the incoming requests match the expected schema.

5. Configure CORS:
   For each resource:
   a. Select the resource.
   b. Choose "Actions" > "Enable CORS".
   c. Configure as needed and click "Enable CORS and replace existing CORS headers".

6. Set up usage plans and API keys (if needed):
   a. Go to "Usage Plans" in the API Gateway console.
   b. Create a new usage plan.
   c. Associate API stages with the usage plan.
   d. Create and associate API keys with the usage plan.

7. Deploy the API:
   a. Select the API.
   b. Choose "Actions" > "Deploy API".
   c. Select a stage (e.g., "prod") or create a new one.
   d. Enter a description for the deployment.
   e. Click "Deploy".

8. Get the invoke URL:
   After deployment, you'll see the invoke URL. This is the base URL for your API endpoints.
