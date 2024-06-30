import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_groq import ChatGroq
import time

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Book Recommendation",
    page_icon="📖",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Get Groq API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize LangChain with ChatGroq model
system_message_100 = SystemMessagePromptTemplate.from_template(
    "Find the top 100 books in the {user_query} genre."
)
system_message_10 = SystemMessagePromptTemplate.from_template(
    "From the list of 100 books, find the top 10 books in the {user_query} genre."
)
system_message_1 = SystemMessagePromptTemplate.from_template(
    "From the top 10 books, which one would you like to read from the {user_query} genre?"
)

thank_you_message = "Thank you for using TaleCompass! Enjoy your reading!"

human_message = HumanMessagePromptTemplate.from_template(
    "{user_query}"
)

prompt_100 = ChatPromptTemplate(
    messages=[
        system_message_100,
        human_message
    ]
)
prompt_10 = ChatPromptTemplate(
    messages=[
        system_message_10,
        human_message
    ]
)
prompt_1 = ChatPromptTemplate(
    messages=[
        system_message_1,
        human_message
    ]
)

llm = ChatGroq(model_name="llama3-8b-8192")
book_chain_100 = LLMChain(prompt=prompt_100, llm=llm)
book_chain_10 = LLMChain(prompt=prompt_10, llm=llm)
book_chain_1 = LLMChain(prompt=prompt_1, llm=llm)

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = []
    st.session_state.top_100_books = []
    st.session_state.top_10_books = []

# Display the chatbot's title on the page
st.title("📖 TaleCompass")


description = """
Welcome to the Top Book Finder!

This application helps you find the best books in any genre using a simple step-by-step workflow:

1. **Top 100 Books**: Start by finding the top 100 books in your chosen genre.
2. **Top 10 Books**: The agent will then narrow down to the top 10 books from the initial list.
3. **Top 1 Book**: Finally, the agent will select the best book for you from the top 10.
4. **Conclusion**: The workflow ends with a thank you message.

Get started by selecting your favorite genre and let the agent do the rest!
"""

# Display a start button
if "start_button_clicked" not in st.session_state:
    st.session_state.start_button_clicked = False

if st.button("Start"):
    st.session_state.start_button_clicked = True

if st.session_state.start_button_clicked:
    # Create an empty container
    typewriter_container = st.empty()

    # Append characters to a string and update the container
    typed_text = ""
    for char in description:
        typed_text += char
        typewriter_container.markdown(typed_text)
        time.sleep(0.004)


# Display the chat history
for message in st.session_state.chat_session:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

# Input field for user's message
user_prompt = st.chat_input("Please enter the genre...")

if user_prompt:
    # Add user's message to chat and display it
    st.session_state.chat_session.append({
        'role': 'user',
        'text': user_prompt
    })
    st.chat_message("user").markdown(user_prompt)

    # Process the user's query to get the top 100 books
    response_100 = book_chain_100.run({"user_query": user_prompt})
    st.session_state.chat_session.append({
        'role': 'assistant',
        'text': response_100
    })
    st.chat_message("assistant").markdown(response_100)
    st.session_state.top_100_books = response_100.split(
        '\n')  # Assuming response_100 is a newline-separated list of books

    # Process to get top 10 books from top 100
    response_10 = book_chain_10.run({"user_query": user_prompt})
    st.session_state.chat_session.append({
        'role': 'assistant',
        'text': response_10
    })
    st.chat_message("assistant").markdown(response_10)
    st.session_state.top_10_books = response_10.split('\n')  # Assuming response_10 is a newline-separated list of books

    # Display top 10 books to user and allow them to choose one
    book_choice = st.radio("Choose a book from the top 10:", st.session_state.top_10_books)
    if book_choice:
        st.session_state.chat_session.append({
            'role': 'user',
            'text': book_choice
        })
        st.chat_message("user").markdown(book_choice)

        # Thank the user
        st.session_state.chat_session.append({
            'role': 'assistant',
            'text': thank_you_message
        })
        st.chat_message("assistant").markdown(thank_you_message)

# Code end
