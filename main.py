import streamlit as st
import os
import re
from autogen import GroupChat, GroupChatManager, UserProxyAgent
from agents.customer_agent import CustomerInfoAgent
from agents.policy_agent import PolicyRetrievalAgent
from agents.decision_agent import LoanDecisionAgent

# -------------------- CONFIG --------------------
# Set OpenAI key
openai_key = "sk-Your-API-KEY"
os.environ["OPENAI_API_KEY"] = openai_key

# Strip ANSI color codes from text
def strip_ansi(text: str) -> str:
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

# Capture print output from agents
conversation_log = []

def capture_print(*args, **kwargs):
    message = " ".join(str(arg) for arg in args)
    clean_msg = strip_ansi(message)
    conversation_log.append(clean_msg)

# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="Loan Decision AI", layout="wide")
st.title("Multi-Agent Loan Approval Assistant")

user_msg = st.text_input("Enter customer query:", "Customer ID 104 applied for a $40,000 loan. What does policy say? Should we approve?")

if st.button("Run Agent Conversation"):
    # Patch built-in print
    import builtins
    original_print = builtins.print
    builtins.print = capture_print

    try:
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

        # Run the conversation
        user.initiate_chat(manager, message=user_msg)

    finally:
        builtins.print = original_print

    # Display the agent conversation
    st.markdown("### Agent Conversation Log")
    for line in conversation_log:
        if line.strip():
            st.markdown(f"```\n{line.strip()}\n```")
