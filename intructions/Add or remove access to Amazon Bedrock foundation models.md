## Add or remove access to Amazon Bedrock foundation models

Before you can use a foundation model in Amazon Bedrock, you must request access to it. If you no longer need access to a model, you can remove access from it.

**Note**: You can't remove request access from the Amazon Titan, Mistral AI, and Meta Llama 3 Instruct models. You can prevent users from making inference calls to these models by using an IAM policy and specifying the model ID. For more information, see Deny access for inference on specific models.

Once access is provided to a model, it is available for all users in the AWS account.
**To add or remove access to foundation models**

1. Make sure you have [permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access-permissions.html) to request access, or modify access, to Amazon Bedrock foundation models.

2. Sign into the Amazon Bedrock console at https://console.aws.amazon.com/bedrock/

3. In the left navigation pane, under **Bedrock configurations**, choose **Model access**.

4. On the **Model access** page, choose **Modify model access**.

5. Select the models that you want the account to have access to and unselect the models that you don't want the account to have access to. You have the following options:

    Be sure to review the **End User License Agreement (EULA)** for terms and conditions of using a model before requesting access to it.

    - Select the check box next to an individual model to check or uncheck it.

    - Select the top check box to check or uncheck all models.

    - Select how the models are grouped and then check or uncheck all the models in a group by selecting the check box next to the group. For example, you can choose to Group by provider and then select the check box next to Cohere to check or uncheck all Cohere models.

6. Choose **Next**.

7. If you add access to Anthropic models, you must describe your use case details. Choose **Submit use case details**, fill out the form, and then select **Submit form**. Notification of access is granted or denied based on your answers when completing the form for the provider.

8. Review the access changes you're making, and then read the **Terms**.

    **Note**: Your use of Amazon Bedrock foundation models is subject to the [seller's pricing terms](https://aws.amazon.com/bedrock/pricing/), EULA, and the [AWS service terms](https://aws.amazon.com/service-terms).

9. If you agree with the terms, choose Submit. The changes can take several minutes to be reflected in the console.

    **Note**: If you revoke access to a model, it can still be accessed through the API for some time after you complete this action while the changes propagate. To immediately remove access in the meantime, add an [IAM policy to a role to deny access to the model](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html#security_iam_id-based-policy-examples-deny-inference).

10. If your request is successful, the **Access status** changes to **Access granted** or **Available to request**.

    **Note**: For AWS GovCloud (US) customers, follow these steps to access models that are available in AWS GovCloud (US):

- AWS GovCloud (US) users must locate their standard AWS account ID associated with their AWS GovCloud (US) account ID. AWS GovCloud (US) users can follow this guide Finding your associated standard AWS account ID, if they don't already know their ID. Navigate to the model access page on Amazon Bedrock console. Select the model(s) that you want to enable. Select Request model access and follow the step-by-step subscription flow.

- AWS GovCloud (US) customers use their standard AWS account ID (which is linked to their AWS GovCloud (US) account ID) to first enable model access. Navigate to the model access page on Amazon Bedrock console in either us-east-1 or us-west-2. Select the model(s) that you want to enable. Select Request model access and follow the step-by-step subscription flow.

- Log into your AWS GovCloud (US) account and navigate to Amazon Bedrock in us-gov-west-1 and follow the same model access sign-up steps. This will grant you a regional entitlement to access the models in us-gov-west-1.

- The model will be accessible to the linked AWS GovCloud (US) account on us-gov-west-1.

If you don't have permissions to request access to a model, an error banner appears. Contact your account administrator to ask them to request access to the model for you or to provide you permissions to request access to the model.
