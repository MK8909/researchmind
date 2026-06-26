






from dotenv import load_dotenv
import os
import streamlit as st
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from tools import web_search, scrape_url

load_dotenv()

groq_key = None
if hasattr(st, "secrets"):
    groq_key = st.secrets.get("GROQ_API_KEY") or st.secrets.get("groq_apikey")
groq_key = groq_key or os.getenv("GROQ_API_KEY") or os.getenv("groq_apikey")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=groq_key,
    temperature=0
)

def build_search_agent():
    return create_agent(model=llm, tools=[web_search])

def build_reader_agent():
    return create_agent(model=llm, tools=[scrape_url])

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}

Write a comprehensive report with the following sections:

# Introduction

# Key Findings
(At least 3 detailed findings)

# Conclusion

# Sources
(List every URL found in the research)

Use professional language and include enough detail.
"""),
])
writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict research reviewer."),
    ("human", """Review the following report.

{report}

Return exactly in this format:

Score: X/10

Strengths:
- ...

Areas to Improve:
- ...

Verdict:
...
"""),
])
critic_chain = critic_prompt | llm | StrOutputParser()
