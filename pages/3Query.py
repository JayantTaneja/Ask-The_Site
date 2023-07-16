import streamlit as st
from utils import (
    key_setter,
    setup_error,
    empty_error,
    db_uploader,
    load_vector_db,
    display_message,
    vector_search,
    ask,
)



st.set_page_config(
    page_title= "Query",
    page_icon= "",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Query")
key_setter()

st.markdown('''

On this page you can upload the vectordb generated in the ```Create Vector DB```
page and use it to query the website crawled earlier.
''')

db_uploader()

st.markdown("""### Vector Similarity Search""")

with st.form("similarity-search"):
    query = st.text_input("Enter your query")
    submit = st.form_submit_button("Find matches")
    if submit:
        setup_error('key', "API Key not found")
        setup_error('file_uploaded', "Vector DB Not Found")
        empty_error(query, "query")

        load_vector_db(path_to_db="temp-uploaded")
        
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
        load_vector_db(path_to_db="temp-uploaded")

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
                    st.markdown(f'''{link}''')
