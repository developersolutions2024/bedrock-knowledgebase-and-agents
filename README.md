# Amazon Bedrock Knowledge Base and Agents ChatBot Solution Demo

## Table of Content
- [Ingest Summary Env](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/ingest_summary)

- [Instructions](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/intructions)

  - [Add or remove access to Amazon Bedrock foundation models](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/intructions/Add%20or%20remove%20access%20to%20Amazon%20Bedrock%20foundation%20models.md)
  - [Create an Amazon Bedrock knowledge base](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/intructions/Create%20an%20Amazon%20Bedrock%20knowledge%20base.md)
  - [Create and configure agent manually](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/intructions/Create%20and%20configure%20agent%20manually.md)
  - [Use action groups to define actions for your agent to perform](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/intructions/Use%20action%20groups%20to%20define%20actions%20for%20your%20agent%20to%20perform.md)

- [Lambda Functions](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/lambda-functions)

  - Amazon API Gateway
    - [agent.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/api-gateway-lambdas/agent.py)
    - [no-agent.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/api-gateway-lambdas/no-agent.py)
    - [uiTranslator](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/uiTranslator.py)
      
  - AWS AppSync
    - [agent.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/appsync-lambdas/agent.py)
    - [no-agent](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/appsync-lambdas/no-agent.py)
    - [uiTranslator](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/appsync-lambdas/uiTranslator.py)
   
  - Independent Functions (work with Both APi Gwy and AppSync)
    - [whoIs.py](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/lambda-functions/whoIs.py)
    - [ingest_summary](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/ingest_summary) (Containerized)
    - [ingest_enrich](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/ingest_enrich) (Containerized)
    - [summary](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/tree/main/summary) (Containerized)

- [Language Configuration](https://github.com/developersolutions2024/bedrock-knowledgebase-and-agents/blob/main/language-config/translation.json)
   
