import streamlit as st
import requests
import json

# Set up your Azure OpenAI API key and endpoint
api_key = "your-actual-api-key"  # Replace with your actual Azure OpenAI API key
endpoint = "https://your-resource-name.openai.azure.com/"  # Replace with your actual Azure OpenAI endpoint
deployment_id = "gpt-4o-realtime-preview"  # Replace with your actual deployment ID
api_version = "2024-10-01"  # Version for the GPT-4o-Realtime-Preview

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Function to send a request to Azure OpenAI API
def get_openai_response(messages):
    data = {
        "messages": messages,
        "max_tokens": 150
    }

    response = requests.post(
        f"{endpoint}openai/deployments/{deployment_id}/chat/completions?api-version={api_version}",
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Define the system prompt (agent characteristics and cultural contingencies)
system_prompt = {
    "role": "system",
    "content": """
    You are an AI agent who comes in support to a landlord who wants to rent his apartment in Milan during the rental negotiation.
    The negotiation is about an apartment in Navigli, Milan, Italy (90 sqm, 2 bedrooms). The initial price requested by the landlord is 1000 euros/month.
    You will listen to the conversation, track the negotiation, and provide suggestions when asked. 
    If asked for the negotiation status, provide insights on the current negotiation stage and suggest next steps if necessary. Your goal should be facilitating the negotiation and try to achieve a win-win outcome, that will satisfy both parties.
    """
}

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = [system_prompt]

# Function to handle user input
def submit_message():
    user_input = st.session_state.input_text
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Get the AI response
    ai_response = get_openai_response(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": ai_response})

    # Clear the input field
    st.session_state.input_text = ""

# Streamlit interface
st.title("AI Negotiation Assistant")

# Text input for user message
st.text_input("You:", key="input_text", placeholder="Write your message here...", on_change=submit_message)

# Display conversation history
for message in st.session_state.conversation:
    if message["role"] == "user":
        st.write(f"You: {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"AI: {message['content']}")

# Additional button to ask for negotiation status
if st.button("Ask for Negotiation Status"):
    status_query = {"role": "user", "content": "Can you tell me the current status of the negotiation?"}
    st.session_state.conversation.append(status_query)
    
    # Get status response from the agent
    status_response = get_openai_response(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": status_response})

# Additional button to ask for suggestions
if st.button("Ask for Suggestions"):
    suggestion_query = {"role": "user", "content": "Can you provide some suggestions for the negotiation?"}
    st.session_state.conversation.append(suggestion_query)
    
    # Get suggestion response from the agent
    suggestion_response = get_openai_response(st.session_state.conversation)
    st.session_state.conversation.append({"role": "assistant", "content": suggestion_response})

