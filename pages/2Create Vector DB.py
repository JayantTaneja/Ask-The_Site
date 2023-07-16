import streamlit as st
from utils import (
    key_setter, 
    empty_error, 
    setup_error,
    generate_sitemap, 
    extract_text, 
    embed,
    show_download
)

st.set_page_config(
    page_title= "Create Vector DB",
    page_icon= "📑",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Create Vector Database")
key_setter()

with st.form("Crawl"):
    base_url = st.text_input("Enter website to crawl", placeholder="karpathy.ai")
    filter = st.text_input("Enter Filter", value="", placeholder="2021")
    excluded = st.text_input("Enter regex pattern for excluded pages", placeholder="pdf")
    submitted = st.form_submit_button("Crawl")
    
    if submitted:
        setup_error("key", "API Key not found")
        empty_error(base_url, "URL")
        generate_sitemap(base_url, filter, excluded)
        pages = extract_text("output_sitemap.xml")
        # embed(pages)
        st.session_state.db_generated = True

if "db_generated" in st.session_state.keys():
    show_download()