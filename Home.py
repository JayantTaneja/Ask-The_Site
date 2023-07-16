import streamlit as st


st.set_page_config(
    page_title= "Ask The Site",
    page_icon= "🔎",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("🔎Ask The Site")


st.markdown('''

Welcome ! This interactive demo is aimed at demonstrating the usage
of Large Language Models (LLMs) and Vector Databases for performing
information retrieval over a website

---
#### Instructions on how to use:
            
Before using any of the available demos, make sure to obtain an OpenAI
API key. (Visit [link](https://platform.openai.com/account/api-keys)) to get
one.
            
##### 1. Pre-loaded Demo:

Head over to [![img](https://img.shields.io/badge/Demo-blue)](Demo) to
try an interactive demo that allows you to query the website of computer
department of J C Bose University Of Science And Technology.
[Website Link](http://www.jcboseust.ac.in/computer_new)

The content of this site(exluding pdf files) was converted into a vector db
over which you can query.
            
---

##### 2. Load your own site
            
**Step 1**: Head over to 
[![img](https://img.shields.io/badge/Create_vector_DB-blue)](Create_Vector_DB)

- Enter your API key in the sidebar
- Type the url of the site you want to use (example : karpathy.ai)
- Enter any filter that must be present (example: tweet)
- Enter regex for patterns to be excluded (example: pdf)
- Hit Crawl

Once the website has been crawled and a vector DB has been generated,
A download button shall appear. Click Download DB to download the vector
database as a zip file.

<br>
<br>
            
**Step 2**: Head over to
[![img](https://img.shields.io/badge/Query-blue)](Query)
            
- Upload the zip file downloaded in **Step 1**

To use similarity search:
- Enter your query in the first text box
- Click Find Matches
- The relevant matching links shall appear
            
To use web chatbot:
- Enter your query in the second text box
- Click Generate Response
- The chatbot (OpenAI GPT 3.5 Turbo) shall generate the
appropriate response.
            
---
            
### Behind the scenes

Head over to
[![img](https://img.shields.io/badge/About-blue)](About) to know more.

---

### How is it different from ChatGPT?

ChatGPT is a fine tuned GPT model capable of performing dialogue
generation or 'chat' based on the knowledge/data stored in its weights.
It is incapable of querying over an existing external knowledge base.

Using a vector db however, we can leverage the general knowledge of
the LLM (GPT 3.5 turbo, in this case) to gain actionable results.

### But Newer GPT-4 Interfaces allow you to search the web?

True, however, they rely on publically available information.
Let's suppose you, at your company/organization have some private data
that you do not want to expose for the purpose of preventing any data leaks.
In such a case, embedding it in a vector db is a good alternative.

Secondly, With the framework LangChain, you have the option of using a 
locally hosted LLM like LLaMa(assuming you have necessary compute power).
This web app aims to showcase the potential of such layouts.  

---

### Who made this demo?

This web app is made by Jayant Taneja:

Checkout : 
[![Link](https://img.shields.io/badge/Jayant_Taneja-blue?logo=Linkedin)](https://www.linkedin.com/in/jayant-taneja/)
[![Link](https://img.shields.io/badge/Jayant_Taneja-black?logo=Github)](https://github.com/JayantTaneja)
''', unsafe_allow_html=True)
