## Use action groups to define actions for your agent to perform

An action group defines actions that the agent can help the user perform. For example, you could define an action group called BookHotel that helps users carry out actions that you can define such as:

  - CreateBooking – Helps users book a hotel.

  - GetBooking – Helps users get information about a hotel they booked.

  - CancelBooking – Helps users cancel a booking.

You create an action group by performing the following steps:

  1. Define the parameters and information that the agent must elicit from the user for each action in the action group to be carried out.

  2. Decide how the agent handles the parameters and information that it receives from the user and where it sends the information it elicits from the user.

To learn more about the components of an action group and how to create the action group after you set it up, select from the following topics:

**Topics**:

- [Define actions in the action group](https://docs.aws.amazon.com/bedrock/latest/userguide/action-define.html)
- [Handle fulfillment of the action](https://docs.aws.amazon.com/bedrock/latest/userguide/action-handle.html)
- [Add an action group to your agent in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-add.html)
- [View information about an action group](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-view.html)
- [Modify an action group](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-edit.html)
- [Delete an action group](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-delete.html)
  

## Add an action group to your agent in Amazon Bedrock

When you [create an agent](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-create.html), you can add action groups to the working draft.

After an agent is created, you can add action groups to it by doing the following steps:

**To add an action group to an agent**

1. Sign in to the AWS Management Console using an [IAM role with Amazon Bedrock permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html), and open the Amazon Bedrock console at https://console.aws.amazon.com/bedrock/.

2. Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

3. Choose **Edit in Agent builder**.

4. In the **Action groups** section, choose **Add**.

5. (Optional) In the **Action group details** section, change the automatically generated **Name** and provide an optional **Description** for your action group.

6. In the **Action group type** section, select one of the following methods for defining the parameters that the agent can elicit from users to help carry out actions:

    - **Define with function details** – Define parameters for your agent to elicit from the user in order to carry out the actions. For more information on adding functions, see [Define function details for your agent's action groups in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-action-function.html).

    - **Define with API schemas** – Define the API operations that the agent can invoke and the parameters . Use an OpenAPI schema that you created or use the console text editor to create the schema. For more information on setting up an OpenAPI schema, see [Define OpenAPI schemas for your agent's action groups in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-api-schema.html)

7. In the **Action group invocation** section, you set up what the agent does after it predicts the API or function that it should invoke and receives the parameters that it needs. Choose one of the following options:

    - **Quick create a new Lambda function** – *recommended* – Let Amazon Bedrock create a basic Lambda function for your agent that you can later modify in AWS Lambda for your use case. The agent will pass the API or function that it predicts and the parameters, based on the session, to the Lambda function.

    - **Select an existing Lambda function** – Choose a [Lambda function that you created previously](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html) in AWS Lambda and the version of the function to use. The agent will pass the API or function that it predicts and the parameters, based on the session, to the Lambda function.

    **Note**: To allow the Amazon Bedrock service principal to access the Lambda function, [attach a resource-based policy to the Lambda function](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-permissions.html#agents-permissions-lambda) to allow the Amazon Bedrock service principal to access the Lambda function.

    - **Return control** – Rather than passing the parameters for the API or function that it predicts to the Lambda function, the agent returns control to your application by passing the action that it predicts should be invoked, in addition to the parameters and information for the action that it determined from the session, in the [InvokeAgent](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent-runtime_InvokeAgent.html) response. For more information, see [Return control to the agent developer by sending elicited information in an InvokeAgent response](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-returncontrol.html).

8. Depending on your choice for the **Action group type**, you'll see one of the following sections:

    - If you selected **Define with function details**, you'll have an **Action group function** section. Do the following to define the function:

        - Provide a **Name** and optional (but recommended) **Description**.

        - To request confirmation from the user before the function is invoked, select **Enabled**. Requesting confirmation before invoking the function may safeguard your application from taking actions due to malicious prompt injections.

        - In the **Parameters** subsection, choose **Add parameter**. Define the following fields:
      
        |   Field 	| Description |
        | --------- | ----------- |
        | Name 	| Give a name to the parameter.|
        | Description (optional) 	| Describe the parameter.|
        | Type 	| Specify the data type of the parameter.|
        | Required 	| Specify whether the agent requires the parameter from the user.|

        - To add another parameter, choose **Add parameter**.

        - To edit a field in a parameter, select the field and edit it as necessary.

        - To delete a parameter, choose the **delete icon** in the row containing the parameter.

    If you prefer to define the function by using a JSON object, choose **JSON editor** instead of **Table**. The JSON object format is as follows (each key in the parameters object is a parameter name that you provide):

    ```
    {
        "name": "string",
        "description": "string",
        "parameters": [
            {
                "name": "string",
                "description": "string",
                "required": "True" | "False",
                "type": "string" | "number" | "integer" | "boolean" | "array"
            }
        ]
    }
    ```
    
    To add another function to your action group by defining another set of parameters, choose Add action group function.

    - If you selected **Define with API schemas**, you'll have an **Action group schema** section with the following options:

        - To use an OpenAPI schema that you previously prepared with API descriptions, structures, and parameters for the action group, select **Select API schema** and provide a link to the Amazon S3 URI of the schema.

        - To define the OpenAPI schema with the in-line schema editor, select **Define via in-line schema editor**. A sample schema appears that you can edit.

            - Select the format for the schema by using the dropdown menu next to **Format**.

            - To import an existing schema from S3 to edit, select **Import schema**, provide the S3 URI, and select **Import**.

            - To restore the schema to the original sample schema, select Reset and then confirm the message that appears by selecting **Reset** again.

9. When you're done creating the action group, choose **Add**. If you defined an API schema, a green success banner appears if there are no issues. If there are issues validating the schema, a red banner appears. You have the following options:

    - Scroll through the schema to see the lines where an error or warning about formatting exists. An X indicates a formatting error, while an exclamation mark indicates a warning about formatting.

    - Select **View details** in the red banner to see a list of errors about the content of the API schema.

10. Make sure to **Prepare** to apply the changes that you have made to the agent before testing it.
