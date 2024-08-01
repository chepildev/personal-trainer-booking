import streamlit as st
import requests
import json
import uuid

# Get the Flowise API key from Streamlit secrets
HF_FLOWISE = st.secrets["HF_FLOWISE"]

# Flowise API URL
API_URL = "https://gennys-personal-trainer-flow.hf.space/api/v1/prediction/366d9675-091d-4f69-aee8-f7c948c0f1ea"

# Headers for the API request
headers = {
    "Authorization": f"Bearer {HF_FLOWISE}",
    "Content-Type": "application/json"
}

# Function to query the Flowise API
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            st.error("Error decoding JSON response.")
            return None
    else:
        st.error(f"API request failed with status code {response.status_code}")
        return None

# Show title and description.
st.title("💬 Personal trainer instagram chat")
st.write(
    "This bot personal trainer assistant that wants to set up a video call with potential clients. "
    "Bot will follow the sales script and send you the link with Calendly to set up a video call. "
    "You are chatting as the potential customer!."
    "Ask your question to test the script flow and give me feedback on what to change."
)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # Generate a unique session ID

 # Button to clear chat history
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Hey how are you?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # # Generate a response using the Flowise API
    # output = query({"question": prompt})

    # Generate a response using the Flowise API with session ID
    output = query({
        "question": prompt,
        "overrideConfig": {
            "sessionId": st.session_state.session_id,
        }
    })

    # Stream the response to the chat
    if output:
        response_message = output.get("text", "No response text.")
        with st.chat_message("assistant"):
            st.markdown(response_message)
        st.session_state.messages.append({"role": "assistant", "content": response_message})
    else:
        st.error("Failed to get a response from the chatbot.")