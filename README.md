# Amazon Bedrock Knowledge Base and Agents ChatBot Solution Demo

## Table of Content
- [Ingest Summary Env](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/ingest_summary)
- [Instructions](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/intructions)
  - [Add or remove access to Amazon Bedrock foundation models](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/intructions/Add%20or%20remove%20access%20to%20Amazon%20Bedrock%20foundation%20models.md)
  - [Create an Amazon Bedrock knowledge base](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/intructions/Create%20an%20Amazon%20Bedrock%20knowledge%20base.md)
  - [Create and configure agent manually](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/intructions/Create%20and%20configure%20agent%20manually.md)
  - [Use action groups to define actions for your agent to perform](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/intructions/Use%20action%20groups%20to%20define%20actions%20for%20your%20agent%20to%20perform.md)
- [Lambda Functions](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/lambda-functions)
  - [Amazon API Gateway](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/lambda-functions/api-gateway-lambdas)
    - [agent.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/api-gateway-lambdas/agent.py)
    - [no-agent.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/api-gateway-lambdas/no-agent.py)
    - [uiTranslator](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/uiTranslator.py)      
  - [AWS AppSync](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/lambda-functions/appsync-lambdas)
    - [agent.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/appsync-lambdas/agent.py)
    - [no-agent](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/appsync-lambdas/no-agent.py)
    - [uiTranslator](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/appsync-lambdas/uiTranslator.py)   
  - Independent Functions (work with Both API Gateway and AppSync)
    - [whoIs.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/whoIs.py)
    - [ingest_summary](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/ingest_summary) (Containerized)
    - [ingest_enrich](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/ingest_enrich) (Containerized)
    - [summary](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/summary) (Containerized)
- [AWS IAM Permissions](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/iam-permissions)
  - Amazon Bedrock 
    - [Knowledge base](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/iam-permissions/knowledge-base-permissions)
      - [Amazon OpenSearch Service](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/knowledge-base-permissions/AmazonBedrockOSSPolicyForKnowledgeBase.json)
      - [Amazon S3](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/knowledge-base-permissions/AmazonBedrockS3PolicyForKnowledgeBase.json)
      - [Foundational Model](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/knowledge-base-permissions/FoundationalModelPolicyForKnowledgeBase.json)
      - [Trusted relationship](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/knowledge-base-permissions/trusted-entities.json)
    - [Agent Role without a Knowledge base](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/bedrock/agent-service-role-without-kb.json)
    - [Agent Role with a Knowledge base](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/bedrock/agent-service-role-with-kb.json)
  - AWS Lambda
    - [agent.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/agent.py.json)
    - [ingest-enrich](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/ingest-enrich.py.json)
    - [ingest-summary](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/ingest-summary.py.json)
    - [summary](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/summary.py.json)
    - [no-agent](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/no-agent.py.json)
    - [uiTranslator](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/uiTranslator.py.json)
    - [whoIs](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/iam-permissions/whoIs.py.json)
- [Language Configuration](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/language-config/translation.json)
   
