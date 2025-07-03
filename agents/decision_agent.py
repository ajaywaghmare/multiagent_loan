from autogen import AssistantAgent

def LoanDecisionAgent(api_key):
    return AssistantAgent(
        name="LoanDecisionAgent",
        system_message=(
            "You make loan approval decisions based on customer profile fields: "
            "credit_score, income, employment_status, and loan_amount_request. "
            "However, before deciding, you MUST request policy guidance from the PolicyRetrievalAgent. "
            "Ask the PolicyRetrievalAgent about relevant loan approval policies using the customer details. "
            "Wait for the policy guidance response before giving your final decision. "
            "Do NOT make decisions on your own without policy information."
        ),
        llm_config={"config_list": [{"model": "gpt-3.5-turbo", "api_key": api_key}]},
        code_execution_config={"use_docker": False}
    )
