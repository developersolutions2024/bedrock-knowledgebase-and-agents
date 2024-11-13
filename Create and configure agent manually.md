## Create and configure agent manually

To create an agent with Amazon Bedrock, you set up the following components:

- The configuration of the agent, which defines the purpose of the agent and indicates the foundation model (FM) that it uses to generate prompts and responses.

- At least one of the following:

    - Action groups that define what actions the agent is designed to perform.

    - A knowledge base of data sources to augment the generative capabilities of the agent by allowing search and query.

You can minimally create an agent that only has a name. To Prepare an agent so that you can [test](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-test.html) or [deploy](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-deploy.html) it, you must minimally configure the following components:
Configuration    | Description |
| -------- | ------- |
| Agent resource role  | The ARN of the [service role with permissions to call API operations on the agent](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-permissions.html)  |
| Foundation model (FM) | An FM for the agent to invoke to perform orchestration   |
|Instructions   | Natural language describing what the agent should do and how it should interact with users    |

You should also configure at least one action group or knowledge base for the agent. If you prepare an agent with no action groups or knowledge bases, it will return responses based only on the FM and instructions and [base prompt templates](https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts.html).

To learn how to create an agent, select the tab corresponding to your method of choice and follow the steps:

**To create an agent**

1. Sign in to the AWS Management Console using an [IAM role with Amazon Bedrock permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html), and open the Amazon Bedrock console at https://console.aws.amazon.com/bedrock/.

2. Select **Agents** from the left navigation pane.

3. In the **Agents** section, choose **Create Agent**.

4. (Optional) Change the automatically generated Name for the agent and provide an optional **Description** for it.

5. Choose **Create**. Your agent is created and you will be taken to the **Agent builder** for your newly created agent, where you can configure your agent.

6. You can continue to the following procedure to configure your agent or return to the Agent builder later.

**To configure your agent**

1. If you're not already in the agent builder, do the following:

    - Sign in to the AWS Management Console using an [IAM role with Amazon Bedrock permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html), and open the Amazon Bedrock console at https://console.aws.amazon.com/bedrock/.

    - Select **Agents** from the left navigation pane. Then, choose an agent in the **Agents** section.

    - Choose **Edit in Agent builder**.

2. In the **Agent details** section, you can set up the following configurations:

   - Edit the **Agent name** or **Agent description**.

   - For the **Agent resource role**, select one of the following options:

        - **Create and use a new service role** – Let Amazon Bedrock create the service role and set up the required permissions on your behalf.

        - **Use an existing service role** – Use a [custom role](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-permissions.html) that you set up previously.

   - For **Select model**, select an FM for your agent to invoke during orchestration.

     By default, models optimized for agents are shown. To see all models supported by Amazon Bedrock Agents, clear **Bedrock Agents optimized**.

     ![bedrock image](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/raw/main/agents-optimized-model-selection.png)

   - In **Instructions for the Agent**, enter details to tell the agent what it should do and how it should interact with users. The instructions replace the $instructions$ placeholder in the orchestration prompt template. Following is an example of instructions:

You are an office assistant in an insurance agency. You are friendly and polite. You help with managing insurance claims and coordinating pending paperwork.

If you expand Additional settings, you can modify the following configurations:

    Code Interpreter – (Optional) Choose whether to enable agent to handle tasks that involve writing, running, testing, and troubleshooting code. For details, see Generate, run, and test code with code interpretation.

    User input – (Optional) Choose whether to allow the agent to request more information from the user if it doesn't have enough information. For details, see Configure agent to request information from user.

    KMS key selection – (Optional) By default, AWS encrypts agent resources with an AWS managed key. To encrypt your agent with your own customer managed key, for the KMS key selection section, select Customize encryption settings (advanced). To create a new key, select Create an AWS KMS key and then refresh this window. To use an existing key, select a key for Choose an AWS KMS key.

    Idle session timeout – By default, if a user hasn't responded for 30 minutes in a session with a Amazon Bedrock agent, the agent no longer maintains the conversation history. Conversation history is used to both resume an interaction and to augment responses with context from the conversation. To change this default length of time, enter a number in the Session timeout field and choose a unit of time.

For the IAM permissions section, for Agent resource role, choose a service role. To let Amazon Bedrock create the service role on your behalf, choose Create and use a new service role. To use a custom role that you created previously, choose Use an existing service role.

    Note

    The service role that Amazon Bedrock creates for you doesn't include permissions for features that are in preview. To use these features, attach the correct permissions to the service role.

    (Optional) By default, AWS encrypts agent resources with an AWS managed key. To encrypt your agent with your own customer managed key, for the KMS key selection section, select Customize encryption settings (advanced). To create a new key, select Create an AWS KMS key and then refresh this window. To use an existing key, select a key for Choose an AWS KMS key.

    (Optional) To associate tags with this agent, for the Tags – optional section, choose Add new tag and provide a key-value pair.

    When you are done setting up the agent configuration, select Next.

In the Action groups section, you can choose Add to add action groups to your agent. For more information on setting up action groups, see Use action groups to define actions for your agent to perform. To learn how to add action groups to your agent, see Add an action group to your agent in Amazon Bedrock.

In the Knowledge bases section, you can choose Add to associate knowledge groups with your agent. For more information on setting up knowledge bases, see Retrieve data and generate AI responses with knowledge bases. To learn how to associate knowledge bases with your agent, see Augment response generation for your agent with knowledge base.

In the Guardrails details section, you can choose Edit to associate a guardrail with your agent to block and filter out harmful content. Select a guardrail you want to use from the drop down menu under Select guardrail and then choose the version to use under Guardrail version. You can select View to see your Guardrail settings. For more information, see Stop harmful content in models using Amazon Bedrock Guardrails.

In the Advanced prompts section, you can choose Edit to customize the prompts that are sent to the FM by your agent in each step of orchestration. For more information about the prompt templates that you can use for customization, see Enhance agent's accuracy using advanced prompt templates in Amazon Bedrock. To learn how to configure advanced prompts, see Advanced prompt templates.

When you finish configuring your agent, select one of the following options:

    To stay in the Agent builder, choose Save. You can then Prepare the agent in order to test it with your updated configurations in the test window. To learn how to test your agent, see Test and troubleshoot agent behavior.

    To return to the Agent Details page, choose Save and exit.
