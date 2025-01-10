import json
from abc import abstractmethod, ABC
from typing import List
from urllib.parse import urlparse
import boto3
import logging
from io import BytesIO
from botocore.config import Config
import os

# LOGGING
log_level = str(os.environ.get('LOGLEVEL', 'ERROR').upper())
logger = logging.getLogger()
logger.setLevel(log_level)
#print(log_level)

# REGION
region = os.environ.get('AWS_REGION', 'us-east-1')
#print(region)

config = Config(
   retries = {
      'max_attempts': 50,
      'mode': 'standard'
   }
)

class Chunker(ABC):
    @abstractmethod
    def chunk(self, text: str) -> List[str]:
        raise NotImplementedError()
        
class SimpleChunker(Chunker):
    def chunk(self, text: str) -> List[str]:
        words = text.split()
        return [' '.join(words[i:i+100]) for i in range(0, len(words), 100)]

prompt_template="""
Human: {prompt}

Assistant:"""



json_schema_sdg = {
  "title":"UN_Sustainable_Development_Goals",
  "type":"object",
  "required":[
    "SDG_1",
    "SDG_2",
    "SDG_3",
    "SDG_4",
    "SDG_5",
    "SDG_6",
    "SDG_7",
    "SDG_8",
    "SDG_9",
    "SDG_10",
    "SDG_11",
    "SDG_12",
    "SDG_13",
    "SDG_14",
    "SDG_15",
    "SDG_16",
    "SDG_17"
  ],
  "properties":{
    "SDG_1":{
      "type":"object",
      "description":"No Poverty. End poverty in all its forms everywhere by ensuring access to resources, basic services, and social protection for everyone, particularly the most vulnerable.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_2":{
      "type":"object",
      "description":"Zero Hunger. End hunger, achieve food security, improve nutrition, and promote sustainable agriculture through better food production and distribution systems.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_3":{
      "type":"object",
      "description":"Good Health and Well-being. Ensure healthy lives and promote well-being for all at all ages through better healthcare access, disease prevention, and health education.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_4":{
      "type":"object",
      "description":"Quality Education. Ensure inclusive and equitable quality education and promote lifelong learning opportunities for all through improved access to education and training.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_5":{
      "type":"object",
      "description":"Gender Equality. Achieve gender equality and empower all women and girls by eliminating discrimination, violence, and harmful practices against women.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_6":{
      "type":"object",
      "description":"Clean Water and Sanitation. Ensure availability and sustainable management of water and sanitation for all through improved infrastructure and water resource management.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_7":{
      "type":"object",
      "description":"Affordable and Clean Energy. Ensure access to affordable, reliable, sustainable, and modern energy for all through renewable energy development and energy efficiency.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_8":{
      "type":"object",
      "description":"Decent Work and Economic Growth. Promote sustained, inclusive, and sustainable economic growth, full and productive employment, and decent work for all.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_9":{
      "type":"object",
      "description":"Industry, Innovation and Infrastructure. Build resilient infrastructure, promote inclusive and sustainable industrialization, and foster innovation.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_10":{
      "type":"object",
      "description":"Reduced Inequalities. Reduce inequality within and among countries by promoting social, economic, and political inclusion of all people.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_11":{
      "type":"object",
      "description":"Sustainable Cities and Communities. Make cities and human settlements inclusive, safe, resilient, and sustainable through better urban planning and management.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_12":{
      "type":"object",
      "description":"Responsible Consumption and Production. Ensure sustainable consumption and production patterns by using resources efficiently and reducing waste.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_13":{
      "type":"object",
      "description":"Climate Action. Take urgent action to combat climate change and its impacts through mitigation and adaptation strategies.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_14":{
      "type":"object",
      "description":"Life Below Water. Conserve and sustainably use the oceans, seas, and marine resources for sustainable development.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_15":{
      "type":"object",
      "description":"Life on Land. Protect, restore, and promote sustainable use of terrestrial ecosystems, sustainably manage forests, combat desertification, halt biodiversity loss.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_16":{
      "type":"object",
      "description":"Peace, Justice and Strong Institutions. Promote peaceful and inclusive societies, provide access to justice for all, and build effective, accountable institutions.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    },
    "SDG_17":{
      "type":"object",
      "description":"Partnerships for the Goals. Strengthen the means of implementation and revitalize the global partnership for sustainable development through cooperation between countries and stakeholders.",
      "required":[
        "detected",
        "context"
      ],
      "properties":{
        "detected":{
          "type":"boolean",
          "default":False,
          "description":"Is this content related to this specific SDG (True) or not (False)"
        },
        "context":{
          "type":"string",
          "default":"NA",
          "description":"How is this content related to this specific SDG"
        }
      }
    }
  }
}


def invoke_model(prompt, client):
    request = {
        "anthropic_version": "bedrock-2023-05-31",    
        "max_tokens": 2000,
        "system": "You are a document reader. You are able to extract and deduct specific requested information from the document. You always report those information in JSON format using a valid JSON schema.",    
        "messages": [
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": prompt }
                ]
            }
            #,{
            #    "role": "assistant",
            #    "content": [
            #        {  "type": "text", "text": """{"meeting_number":""" }  # Prefill here
            #    ]
            #}
        ],
        "temperature": 0,
        "top_p": 0.9,
        "top_k": 100,
        "tools": [
            {
                "name": "SDG_analysis",
                "description": "Today, humanity exists in an interconnected globe with severe collective problems such as climate change or poverty/inequalities. The United Nations established the Sustainable Development Goals (SDGs) as a reference to address such conflicts and give better lives for people in all areas of our planet. Their main aim is to tackle these challenges along with others to make the world more sustainable for future generations. There are 17 goals defined in SDGs and they are focused on the sustainable development of our future generations. This tool reads the document / text provided in input. For each SDG, the tool repports if there is a relation with the document (boolean) and describe this relation (string). The output is a JSON document. The JSON document respect a JSON schema",
                "input_schema": json_schema_sdg
                
            }
        ],
        "tool_choice": {
            "type" :  "tool",
            "name" : "SDG_analysis",
        }
    }  

# anthropic.claude-3-5-haiku-20241022-v1:0
# us.anthropic.claude-3-haiku-20240307-v1:0
# us.anthropic.claude-3-5-sonnet-20241022-v2:0
    response = client.invoke_model(
        body=json.dumps(request),
        modelId="us.anthropic.claude-3-haiku-20240307-v1:0"
        #modelId="us.anthropic.claude-3-haiku-20240307-v1:0"
    )
    result = json.loads(response['body'].read().decode())
    content = result["content"]
    tool_use = ""
    for c in content:
        if c["type"] == "tool_use":
            tool_use = c['input']
    return tool_use


def lambda_handler(event, context):
    print(event)
    logger.info('## INPUT')
    logger.info(event)

    agent = event['agent']
    actionGroup = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    content = next((item for item in parameters if item["name"] == "content"), '')["value"]
    print("TOPIC : " + str(content))

    bedrock = boto3.client('bedrock-runtime', config=config, region_name = region)

    logger.info('## SDG')   
    sdg = invoke_model(content,bedrock)     
    logger.info(sdg)
    print(sdg)


    response_body = {
        'TEXT': {
            'body': json.dumps(sdg)
        }
    }


    function_response = {
        'actionGroup': event['actionGroup'],
        'function': event['function'],
        'functionResponse': {
            'responseBody': response_body
        }
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    action_response = {
        'messageVersion': event['messageVersion'], 
        'response': function_response
        #'sessionAttributes': session_attributes,
        #'promptSessionAttributes': prompt_session_attributes
    }
    print(str(action_response))
        
    return action_response

    
