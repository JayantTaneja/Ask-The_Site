import streamlit as st





st.set_page_config(
    page_title= "About",
    page_icon= "",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("About")

st.markdown('''
---
### What's going on ?

What you see in the prev demos is a combination of vector databases and
LangChain Framework to facilitate querying a website.

<center><img src = "./app/static/diagram1.jpg" width = 85%></img></center>

---
           
### How does it work ?

#### 1. Sitemap Generation: 

We Begin by crawling the web URL to generate the ```XML``` sitemap.

<center><img src = "./app/static/diagram2.jpg" width = 85%></img></center>

<br>
<br>
            
The resulting sitemap looks like:

<details>
     
```xml
<?xml version="1.0" encoding="UTF-8"?>
	<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
		<url>
			<loc>
				https://site.com/page1.html
			</loc>
		</url>
		<url>
			<loc>
				https://site.com/page2.html
			</loc>
		</url>
		<url>
			<loc>
				https://site.com/page2/page3.html
			</loc>
		</url></urlset>
```

</details>
            
<br>
<br>
            
#### 2. Crawling

Next step is to crawl the website using the sitemap and extract the text 
from each page
            
<center><img src = "./app/static/diagram3.jpg" width = 85%></img></center>


<br>
<br>

#### 3. Splitting and Embedding

Once we have all the text data, it is split into small chunks and subsequently
embedded into a vector database.

<center><img src = "./app/static/diagram4.jpg" width = 85%></img></center>

<br>
<br>
''', unsafe_allow_html=True)

video1 = open(r"static/diagram5.mp4", "rb")
st.video(video1.read())

st.markdown('''

#### 4. Usage [![See](https://img.shields.io/badge/Click_To_Try_Demo-blue)](Demo)

We can now use the vectordb generated to:

- Perform Similarity Search:
        Use Cosine Similarity to find the documents containing content
        relevant to out query (Fast, inexpensive but less accurate)
        

- Use LLMs like ```gpt 3.5 turbo```: 
        To process our documents using natural
        language

''', unsafe_allow_html=True)