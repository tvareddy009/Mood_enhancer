import random
import streamlit as st
from streamlit_chat import message
import os 
import tempfile
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)


os.environ["OPENAI_API_KEY"] = "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"
llm = ChatOpenAI(model="gpt-4")
memory = ConversationBufferMemory(k=5, return_messages=True)
system = SystemMessagePromptTemplate.from_template(
    template="You are an expert in charming conversation, engaging in playful and light-hearted flirting that brings a smile to the user's face. Respond warmly and with wit to each message, staying respectful, refined, and within appropriate limits. Avoid any use of emojis, and keep the language tasteful and sophisticated, with no vulgarity. Each response should make the user feel valued and delighted, balancing warmth with a subtle allure. Keep the tone classy, focusing on making the conversation enjoyable and memorable."
)
human = HumanMessagePromptTemplate.from_template(template="{input}")
prompt = ChatPromptTemplate.from_messages([system, MessagesPlaceholder(variable_name="history"), human])

# Define conversation chain
conversation = LLMChain(memory=memory, prompt=prompt, llm=llm, verbose=True)
taglines = [
    "Ready to sweep you off your feet!",
    "Bringing charm to every chat.",
    "Turning up the charm, just for you!",
    "Making hearts race, one message at a time.",
    "Your charming chatbot awaits!",
    "Prepare for some heart-fluttering responses!",
    "Let's make this conversation unforgettable.",
]

# Flirt function to generate response
def flirt(query):
    response = conversation.predict(input=f"Query:\n{query}")
    return response

# Function to convert text to speech and return audio file path



# Streamlit page setup
st.set_page_config(page_title="Mood Enhancer", layout="centered")
st.markdown("<h1 style='text-align: center; font-family: italic; color: #FF69B4;'>Mood Enhancer💕</h1>", unsafe_allow_html=True)
st.markdown('<br>' * 2, unsafe_allow_html=True)

# Initialize session state for storing requests and responses
if "requests" not in st.session_state:
    st.session_state["requests"] = []
if "responses" not in st.session_state:
    st.session_state["responses"] = []

# Containers for displaying conversation
response_container = st.container()
textcontainer = st.container()

# Input text box and handling user input
with textcontainer:
    query = st.text_input("Send your charming message to the mood enhancer!", value='', key="input", help="Enter your message here")
    if query:
        with st.spinner("The Mood Enhancer is crafting a charming response..."):
            # Generate response using the flirt function
            response = flirt(query)
        
        # Store the user query and bot response in session state
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)

# Display conversation history with audio output
with response_container:
    if st.session_state["responses"]:
        for i in range(len(st.session_state["responses"])):
            # Display bot response
            message(st.session_state["responses"][i], key=str(i))
            
    
            # Display user message right after the bot response
            if i < len(st.session_state["requests"]):
                message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
