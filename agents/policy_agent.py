from autogen import AssistantAgent
from rag.query_vector_db import retrieve_relevant_policies

def PolicyRetrievalAgent(api_key):
    return AssistantAgent(
        name="PolicyRetrievalAgent",
        system_message=(
            "You are a policy assistant. When asked a policy-related question, "
            "you MUST call the function `retrieve_relevant_policies(query)` with a clearly written query. "
            "You must NOT respond directly or generate answers from your own knowledge. "
            "Only call the function and return exactly what it returns. "
            "Example: Call `retrieve_relevant_policies` with query = 'Loan approval policy for credit score 300 and $110,000 loan request'. "
            "Never answer in your own words. Never summarize. Only call the function."
        ),
        llm_config={
            "config_list": [
                {
                    "model": "gpt-3.5-turbo",
                    "api_key": api_key
                }
            ],
            "functions": [
                {
                    "name": "retrieve_relevant_policies",
                    "description": "Retrieve relevant policy lines using semantic similarity",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "A natural language query describing the policy need"
                            }
                        },
                        "required": ["query"]
                    }
                }
            ]
        },
        function_map={
            "retrieve_relevant_policies": retrieve_relevant_policies
        }
    )
