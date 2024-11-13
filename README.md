# Amazon Bedrock Knowledge Base and Agents


## Add or remove access to Amazon Bedrock foundation models

Before you can use a foundation model in Amazon Bedrock, you must request access to it. If you no longer need access to a model, you can remove access from it.

**Note**: You can't remove request access from the Amazon Titan, Mistral AI, and Meta Llama 3 Instruct models. You can prevent users from making inference calls to these models by using an IAM policy and specifying the model ID. For more information, see Deny access for inference on specific models.

Once access is provided to a model, it is available for all users in the AWS account.
**To add or remove access to foundation models**

1. Make sure you have permissions to request access, or modify access, to Amazon Bedrock foundation models.

2. Sign into the Amazon Bedrock console at https://console.aws.amazon.com/bedrock/

.

In the left navigation pane, under Bedrock configurations, choose Model access.

On the Model access page, choose Modify model access.

Select the models that you want the account to have access to and unselect the models that you don't want the account to have access to. You have the following options:

Be sure to review the End User License Agreement (EULA) for terms and conditions of using a model before requesting access to it.

    Select the check box next to an individual model to check or uncheck it.

    Select the top check box to check or uncheck all models.

    Select how the models are grouped and then check or uncheck all the models in a group by selecting the check box next to the group. For example, you can choose to Group by provider and then select the check box next to Cohere to check or uncheck all Cohere models.

Choose Next.

If you add access to Anthropic models, you must describe your use case details. Choose Submit use case details, fill out the form, and then select Submit form. Notification of access is granted or denied based on your answers when completing the form for the provider.

Review the access changes you're making, and then read the Terms.



## How to create a knowledge base



## How to create an agent



## How to create an action group
