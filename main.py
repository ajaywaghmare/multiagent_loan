import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autogen import GroupChat, GroupChatManager, UserProxyAgent
from agents.customer_agent import CustomerInfoAgent
from agents.policy_agent import PolicyRetrievalAgent
from agents.decision_agent import LoanDecisionAgent

openai_key = "sk-YOUR-KEY"

# Create agents
user = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False}
)

customer_agent = CustomerInfoAgent(openai_key)
policy_agent = PolicyRetrievalAgent(openai_key)
decision_agent = LoanDecisionAgent(openai_key)

# Group chat setup
group_chat = GroupChat(
    agents=[user, customer_agent, policy_agent, decision_agent],
    messages=[],
    max_round=8,
)


manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={
        "config_list": [{"model": "gpt-3.5-turbo", "api_key": openai_key}]
    }
)

# Start the conversation
user.initiate_chat(
    manager,
    message="Customer ID 123 applied for a $110,000 loan. What does policy say? Should we approve?"
)



