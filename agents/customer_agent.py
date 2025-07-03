from autogen import AssistantAgent
from utils.mock_data import get_customer_profile

def CustomerInfoAgent(api_key):
    return AssistantAgent(
        name="CustomerInfoAgent",
        system_message=(
            "Your role is to fetch customer profile data only by calling the function "
            "`get_customer_profile(customer_id)` whenever a customer ID is mentioned. "
            "Do NOT make up or assume values. You must use the function output. "
            "Return the following fields from the function response: credit_score, income, and employment_status."
        ),
        code_execution_config={"use_docker": False},
        llm_config={
            "config_list": [{
                "model": "gpt-3.5-turbo",
                "api_key": api_key
            }],
            "functions": [
                {
                    "name": "get_customer_profile",
                    "description": "Retrieve the customer profile details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_id": {
                                "type": "integer",
                                "description": "The ID of the customer to retrieve"
                            }
                        },
                        "required": ["customer_id"]
                    }
                }
            ]
        },
        function_map={
            "get_customer_profile": get_customer_profile
        }
    )



