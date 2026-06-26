from dotenv import load_dotenv
import os

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from tools import web_search, scrape_url

load_dotenv()

# ---------------------------------------------------
# GROq LLM
# ---------------------------------------------------


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("groq_apikey"),
    temperature=0
)
'''
llm = ChatOpenAI(
    model="grok-4",
    temperature=0,
    api_key=os.getenv("grok_apikey"),
    base_url="https://api.x.ai/v1",
)'''

# ---------------------------------------------------
# SEARCH AGENT(1st agent)
# ---------------------------------------------------

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],      ## ei agent the web_search tool use korbe, jeta tavily API theke search result return korbe.
    )

# ---------------------------------------------------
# READER AGENT( 2nd agent)
# ---------------------------------------------------

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
    )

# ---------------------------------------------------
# WRITER CHAIN(produce the final report from the research gathered by the agents)
# ---------------------------------------------------

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured and insightful reports."
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

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
"""
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ---------------------------------------------------
# CRITIC CHAIN
# ---------------------------------------------------

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a strict research reviewer."
    ),
    (
        "human",
        """Review the following report.

{report}

Return exactly in this format:

Score: X/10

Strengths:
- ...

- ...

Areas to Improve:
- ...

- ...

Verdict:
...
"""
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()