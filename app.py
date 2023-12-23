import streamlit as st
import requests
import datetime

# Define a function to get responses from Rasa
def get_bot_response(message):
    payload = {
        "sender": "user",
        "message": message
    }
    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json=payload)
    if r.status_code == 200 and r.json():
        return [resp.get('text') for resp in r.json()]  # Return a list of messages
    else:
        return ["Sorry, I'm having trouble understanding that."]

# Streamlit app layout
st.title('University Chatbot')
st.write('To end the conversation, type "stop".')
st.write('Hey. How can I help you today?')

# Initialize session state to store conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    

# Display conversation in a more conversational style
def display_conversation():
    for i, line in enumerate(st.session_state.conversation):
        # Generate a unique key using the index and current timestamp
        unique_key = f"{i}_{datetime.datetime.now().timestamp()}"
        if i % 2 == 0:  # User messages
            st.text_area(f"You:", value=line, height=10, key=f"user_{unique_key}")
        else:  # Bot responses
            if isinstance(line, list):
                for j, bot_message in enumerate(line):
                    st.text_area(f"Bot:", value=bot_message, height=10, key=f"bot_{unique_key}_{j}")
            else:
                st.text_area(f"Bot:", value=line, height=10, key=f"bot_{unique_key}")

display_conversation()

# Handle user input
def handle_input():
    user_input = st.session_state.user_input
    if user_input.lower() == 'stop':
        st.write("You have ended the conversation. Refresh the page to start over.")
        return
    if user_input:
        st.session_state.conversation.append(user_input)
        bot_response = get_bot_response(user_input)
        st.session_state.conversation.append(bot_response)
        st.session_state.user_input = ""

# User input text box with the on_change callback
user_input = st.text_input("You:",
                           key="user_input",
                           on_change=handle_input)

