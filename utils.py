import streamlit as st
import requests
import xmltodict
import shutil
import zipfile

from bs4 import BeautifulSoup
from time import sleep

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

from openai.error import AuthenticationError

from crawl import crawl



#-----------------------Setup And Other Utilities---------------------------

def load_embedding_function()->None:
    '''
    Loads LangChain's OpenAI Embeddings object into session state
    '''

    st.session_state.embeddings = OpenAIEmbeddings(
        openai_api_key=st.session_state.key
    )

def load_vector_db(path_to_db = "embeddings"):
    '''
    Loads ChromaDB into session state

    Args:
        path_to_db : (str) Path to folder containing ChromaDB embeddings
    '''

    st.session_state.vectordb = Chroma(
        persist_directory=path_to_db, 
        embedding_function=st.session_state.embeddings
    )

def load_chain():
    '''
    Loads LangChain's ```RetrievalQAWithSourcesChain``` into session state
    '''
   
    st.session_state.chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(
            temperature=0, 
            openai_api_key=st.session_state.key
        ), 
        chain_type="stuff",
        retriever=st.session_state.vectordb.as_retriever()
    )

def display_message(string:str, time_delay:float = 0.04):
    '''
    Smoothly displays the text, chunk wise

    Args:
        string : (str) String t be displayed
        time_delay : (float) Time delay in seconds between each chunk
    '''
    chunks = string.split()
    curr = ""
    place_holder = st.markdown(curr)
    
    for chunk in chunks:
        curr = curr + chunk + " "
        place_holder.markdown(curr + "▌")
        sleep(time_delay)
    place_holder.markdown(curr)

def key_setter():
    '''
    Displays Key Input Form in the side bar and loads it into session state
    '''

    with st.sidebar:
        with st.form("set_key"):
            key = st.text_input("OpenAI API Key", type="password")
            set_key = st.form_submit_button("Set Key")
            
            if set_key:
                if(key == ""):
                    st.error("Empty Key")
                    st.stop()
                st.session_state.key = key
                st.success("Key set successfully !")

def empty_error(var:str, object_name:str):
    '''
    Displays 'Empty "Object" ' error message if variable str is an
    empty string

    Args:
        var : (str) Variable to check
        object_name : (str) Object name to show
    '''
    if(var == ""):
        st.error("Empty {}".format(object_name))
        st.stop()

def setup_error(object:str, message:str):
    '''
    Displays ```message``` error if ```object``` is not in session state

    Args:
        object : (str) Object to be checked
        message : (str) Error message to be displayed 
    '''
    if object not in st.session_state.keys():
        st.error(message)
        st.stop()


#-------------------------Vector DB Creation------------------------------


def generate_sitemap(
        base_url:str, 
        filter:str, 
        excluded:str
    ):
    '''
    Crawls the Site to generate an XML sitemap

    Args:
        base_url : (str) URL to crawl
        filter : (str) Filter that must be present in links to be crawled
        excluded : (str) Regex for links to be excluded from search
    '''

    with st.spinner("Generating Sitemap"):
        crawl("https://" + base_url, filter, excluded)
        st.success("Sitemap generated")


def extract_text_from(url:str)->str:
    '''
    Crawls a page and extracts text from it

    Args:
        url : (str) Site to be crawled

    Returns:
        (str) Text content of the url
    '''

    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    return '\n'.join(line for line in lines if line)


def extract_text(path_to_sitemap:str)->list[dict]:
    '''
    Crawls the links in sitemap and extracts text from them

    Args:
        path_to_sitemap : (str) Path to the sitemap (local)

    Returns:
        List of dicts in the format 
        ```
        {
            'text':text, 
            'source': url
        }
        ```
    '''
    with st.spinner("Loading Sitemap into memory"):
        with open(path_to_sitemap, "r") as file:
            xml = file.read()
    
    raw = xmltodict.parse(xml)

    with st.spinner("Crawling Site..."):
        pages = []

        if 'url' not in raw['urlset']:
            st.error("No matching pages with given filter")
            st.stop()

        n = len(raw['urlset']['url'])
        
        if(n == 1):
            url = raw['urlset']['url']['loc']
            pages.append({'text': extract_text_from(url), 'source': url})
        
        else:
            pbar = st.progress(0, text="0 % Completed")
            
            for idx, info in enumerate(raw['urlset']['url']):
                url = info['loc']
                pages.append({'text': extract_text_from(url), 'source': url})
                pbar.progress((idx+1)/n, text="{} % Completed".format((idx*100)//n))
            pbar.progress(100, text="100% Complete")
    st.success("Site crawled successfuly !")
    return pages

def split_into_chunks(pages:list):
    '''
    Splits pages into chunks using LangChain ```CharacterTextSplitter```

    Args:
        pages (list): List of pages as returned by ```extract_from_text```
    
    Returns:
        (docs, metadatas) (tuple): Chunked docs and their metadatas
    '''

    text_splitter = CharacterTextSplitter(chunk_size=1000, separator="\n")
    docs, metadatas = [], []
    with st.spinner("Splitting Data Into Chunks..."):
        pbar = st.progress(0, text="0 % Complete")
        
        for idx, page in enumerate(pages):
            splits = text_splitter.split_text(page['text'])
            docs.extend(splits)
            metadatas.extend([{"source": page['source']}] * len(splits))
            print(f"Split {page['source']} into {len(splits)} chunks")
        
            pbar.progress(idx/len(pages), "{} % Complete".format((idx*100)//len(pages)))
        
        pbar.progress(100, text="100% Complete")
    
    st.success("Text Successfully Split into Chunks of size 1000")

    return (docs, metadatas)

def embed(pages:list):
    '''
    Embeds pages into ChromaDB using OpenAIEmbeddings

    Args:
        pages : List of pages
    '''
    docs, metadatas = split_into_chunks(pages)
    
    st.session_state.embedding_function = OpenAIEmbeddings(
        openai_api_key=st.session_state.key
    )
    
    try:
        with st.spinner("Beginning Embedding"):
            vectordb = Chroma.from_texts(
                docs, 
                st.session_state.embedding_function, 
                metadatas=metadatas, 
                persist_directory="temp-embeddings"
            )
            vectordb.persist()
        
            st.success("Embeddings Created")
    except AuthenticationError:
        st.error("Authentication Error, check your API key")
        st.stop()


def show_download():
    '''
    Zips the ChromaDB embeddings and facilitates download
    '''
    shutil.make_archive('db', 
                        'zip',
                        'temp-embeddings')

    with open("db.zip", "rb") as file:
        st.download_button("Download DB", file, file_name="db.zip")


def db_uploader():
    uploaded_file = st.file_uploader("Upload Vector DB", type=["zip"])

    if uploaded_file is not None:
        with st.spinner("Extracting Contents"):
            bytes_data = uploaded_file.getvalue()
            
            with open("temp.zip", "wb") as f:
                f.write(bytes_data)
            
            with zipfile.ZipFile('temp.zip', 'r') as zip_ref:
                zip_ref.extractall('temp-uploaded')

            st.session_state.file_uploaded = True


#---------------------LLM Prompting And DB Search-----------------------------

def ask(question:str, base_prompt:str = ""):
    
    load_chain()

    prompt = {
        "question" : base_prompt + question
    }

    try:
        response = st.session_state.chain(prompt)
    except AuthenticationError:
        st.error("Authentication Error, check your API key")
        st.stop()

    result = {
        "Answer" : response["answer"],
        "Links" : [i.strip() for i in response["sources"].split('\n-')]
    }

    return result


def vector_search(query:str):
    if 'vectordb' not in st.session_state.keys():
        load_vector_db()
    
    try:
        docs = st.session_state.vectordb.similarity_search(query)
    except AuthenticationError:
        st.error("Authentication Error, check your API key")
        st.stop()

    links = []
    for doc in docs:
        links.append(doc.metadata["source"])
    return links