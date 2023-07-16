import streamlit as st
from utils import key_setter, setup_error, empty_error, display_message, vector_search, ask

st.set_page_config(
    page_title= "Demo",
    page_icon= "🏎️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Demo")


key_setter()

st.markdown('''
            
This page contains demo of 2 main LLM based retrieval methods for websites.
The content of www.jcboseust.ac.in/computer_new was embedded in a vector
databse which can then be used to perform

1. Similarity Search
2. LLM based Natural Language Querying and Response 

---
            
#### Vector DB Search
            
Type your query and the app will perform similarity search in the vector
database to find the most relevant matches based on page contents.
''')

with st.form("similarity-search"):
    query = st.text_input("Enter your query")
    submit = st.form_submit_button("Find matches")
    if submit:
        setup_error('key', "API Key not found")
        empty_error(query, "query")
        with st.spinner("Finding Relevant Matches"):
            links = vector_search(query)
        
        if len(links) == 0:
            st.write("No relevant links found")
        else:
            display_message("Here are some relevant matches to your query: ")
            for link in links:
                st.markdown(link)


st.write("---")

st.markdown('''

#### Web Document ChatBot

Type your question below to get Natural Language response from the chatbot
''')

with st.form("chatbot"):
    query = st.text_input("Enter your question")
    submit = st.form_submit_button("Generate Response")
    if submit:
        setup_error('key', "API Key not found")
        empty_error(query, "query")

        with st.spinner("Fetching Results"):
            result = ask(query)
        
        with st.chat_message("assistant"):
            display_message(result["Answer"])
            
            st.markdown('''
            ---
            ''')

            if(len(result["Links"]) > 0):
                display_message('''
                Here are some of the links where you can find the information above:
                ''')

                for link in result["Links"]:
                    st.markdown(f'''[{link}]({link})''')
