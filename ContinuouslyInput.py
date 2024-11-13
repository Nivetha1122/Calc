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
#llm
from langchain.chains import LLMChain
from langchain.llms import AzureOpenAI
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from azure.search.documents import SearchClient

# Initialize Azure OpenAI
llm = AzureOpenAI(
    deployment_name="your-deployment-name",
    model="text-davinci-003",
    temperature=0.7,
    max_tokens=1000,
)

# Initialize Azure AI Search Client
search_client = SearchClient(endpoint="your-search-endpoint", index_name="your-index-name", credential="your-credentials")

# Query Azure AI Search
search_results = search_client.search(query="Your search query")

# Chunking and Filtering
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
chunks = []
for result in search_results:
    chunks.extend(text_splitter.split_text(result['content']))

# Filtering chunks (example: based on keyword)
filtered_chunks = [chunk for chunk in chunks if "relevant_keyword" in chunk]

# Prompt Construction
prompt = f"User Query: {user_query}\n\nRelevant Results:\n{'\n'.join(filtered_chunks[:3])}"

# Run the LLM
response = llm(prompt)
print(response)
