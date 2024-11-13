import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Initialize Azure client with endpoint and key
def authenticate_client():
    key = "your_azure_key"
    endpoint = "your_endpoint"
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

client = authenticate_client()

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display chat history
st.title("Azure AI Chatbot")
for message in st.session_state["chat_history"]:
    st.write(message)

# User input field
user_input = st.text_input("Enter your query:")

# Button to submit the query
if st.button("Send"):
    if user_input:
        # Display user's query
        st.session_state["chat_history"].append(f"User: {user_input}")
        
        # Azure AI query
        response = client.recognize_entities([{"id": "1", "text": user_input}])
        model_response = response[0].entities[0].text  # Simplified; adjust as needed
        
        # Append model's response
        st.session_state["chat_history"].append(f"Bot: {model_response}")
        
        # Clear input after each submission
        st.experimental_rerun()
