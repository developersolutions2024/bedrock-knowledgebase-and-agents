## Create an Amazon Bedrock knowledge base

You can create an Amazon Bedrock knowledge base to retrieve information from your proprietary data and generate responses to answer natural language questions. As part of creating a knowledge base, you configure a data source and a vector store of your choice.

**Note**: You can’t create a knowledge base with a root user. Log in with an IAM user before starting these steps.

**To create a knowledge base**

1. Sign in to the AWS Management Console using an [IAM role with Amazon Bedrock permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html), and open the Amazon Bedrock console at https://console.aws.amazon.com/bedrock/.

2. From the left navigation pane, select **Knowledge bases**.

3. In the **Knowledge bases** section, select the create button.

4. Provide knowledge base details and set up the following configurations.

    - (Optional) Change the default name and provide a description for your knowledge base.

    - Choose an AWS Identity and Access Management (IAM) role that provides Amazon Bedrock permission to access other required AWS services. You can let Amazon Bedrock create the service role or choose a [custom role that you have created](https://docs.aws.amazon.com/bedrock/latest/userguide/kb-permissions.html).

    - (Optional) Add tags to your knowledge base. For more information, see Tagging Amazon Bedrock resources.

    - Go to the next section.

5. Configure your data source to use for the knowledge base.

    - Follow the connection configuration steps for your selected data source. See Supported data sources to select your data source and follow the console connection configuration steps.

    - (Optional) Configure the advanced settings as part the data source configuration.

        For KMS key settings, you can choose either a custom key or use the default provided data encryption key.

        While converting your data into embeddings, Amazon Bedrock encrypts your transient data with a key that AWS owns and manages, by default. You can use your own KMS key. For more information, see Encryption of transient data storage during data ingestion.

        For data deletion policy settings, you can choose either:

        - Delete: Deletes all data from your data source that’s converted into vector embeddings upon deletion of a knowledge base or data source resource. Note that the vector store itself is not deleted, only the data. This flag is ignored if an AWS account is deleted.

        - Retain: Retains all data from your data source that’s converted into vector embeddings upon deletion of a knowledge base or data source resource. Note that the vector store itself is not deleted if you delete a knowledge base or data source resource.

    - Configure the content chunking and parsing settings as part the data source configuration.

        Choose one of the follow chunking options:

        - Fixed-size chunking: Content split into chunks of text of your set approximate token size. You can set the maximum number of tokens that must not exceed for a chunk and the overlap percentage between consecutive chunks.

        - Default chunking: Content split into chunks of text of up to 300 tokens. If a single document or piece of content contains less than 300 tokens, the document is not further split.

        - Hierarchical chunking: Content organized into nested structures of parent-child chunks. You set the maximum parent chunk token size and the maximum child chunk token size. You also set the absolute number of overlap tokens between consecutive parent chunks and consecutive child chunks.

        - Semantic chunking: Content organized into semantically similar text chunks or groups of sentences. You set the maximum number of sentences surrounding the target/current sentence to group together (buffer size). You also set the breakpoint percentile threshold for dividing the text into meaningful chunks. Semantic chunking uses a foundation model. View [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) for information on the cost of foundation models.

        - No chunking: Each document is treated as a single text chunk. You might want to pre-process your documents by splitting them into separate files.

        **Note**: You can’t change the chunking strategy after you have created the data source.

        You can choose to use Amazon Bedrock’s foundation model for parsing documents to parse more than standard text. You can parse tabular data within documents with their structure intact, for example. [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) for information on the cost of foundation models.

        You can choose to use an AWS Lambda function to customize your chunking strategy and how your document metadata attributes/fields are treated and ingested. Provide the Amazon S3 bucket location for the Lambda function input and output.

    - Go to the next seciton.

6. Choose an available embeddings model to convert your data into vector embeddings for the knowledge base. See [supported embeddings models](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-supported.html) for information.

7. Choose a vector store to store the vector embeddings for your knowledge base. See [supported vector stores](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-setup.html) for information.

    - **Quick create a new vector store** – Amazon Bedrock creates an Amazon OpenSearch Serverless vector search collection for you. With this option, a public vector search collection and vector index is set up for you with the required fields and necessary configurations. After the collection is created, you can manage it in the Amazon OpenSearch Serverless console or through the AWS API. For more information, see Working with vector search collections in the Amazon OpenSearch Service Developer Guide. If you select this option, you can optionally enable the following settings:

        - To enable redundant active replicas, such that the availability of your vector store isn't compromised in case of infrastructure failure, select Enable redundancy (active replicas).

        **Note**: We recommend that you leave this option disabled while you test your knowledge base. When you're ready to deploy to production, we recommend that you enable redundant active replicas. For information about pricing, see [Pricing for OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-overview.html#serverless-pricing)

        - To encrypt the automated vector store with a customer managed key select Add customer-managed KMS key for Amazon OpenSearch Serverless vector – optional and choose the key. For more information, see Encryption of information passed to Amazon OpenSearch Service.

    - **Select a vector store you have created** – Select the service for the vector store that you have already created. Fill in the fields to allow Amazon Bedrock to map information from the knowledge base to your vector store, so that it can store, update, and manage vector embeddings. For more information about the fields, see Set up your own supported vector store.

    **Note**: If you use a database in Amazon OpenSearch Serverless, Amazon Aurora, or MongoDB Atlas, you need to have configured the fields under Field mapping beforehand. If you use a database in Pinecone or Redis Enterprise Cloud, you can provide names for these fields here and Amazon Bedrock will dynamically create them in the vector store for you.

8. Go to the next section.

9. Check the configuration and details of your knowledge base. Select the edit button in any section that you need to modify. When you are satisfied, select the create button.

10. The time it takes to create the knowledge base depends on your specific configurations. When the knowledge base creation has completed, the status of the knowledge base changes to either state it is ready or available.



### After you've created a knowledge base, you might have to set up the following security configurations:

**Topics**:

- [Set up data access policies for your knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-create.html#kb-create-security-data)
- [Set up network access policies for your Amazon OpenSearch Serverless knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-create.html#kb-create-security-network)

