from langchain.tools import tool 
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os 
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("tavily_apikey"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    results = tavily.search(query=query,max_results=5)

    '''query': 'who goin to win uttar pradesh electuion?',
    'follow_up_questions': None,
    'answer': None,
    'images': [],
    'results': [
        {
            'url': 
'https://www.quora.com/Will-the-BJP-win-the-2027-Uttar-Pradesh-state
-elections',
            'title': 'Will the BJP win the 2027 Uttar Pradesh state 
elections? - Quora',
            'content': 'It is going to be something challenging for 
BJP to win the upcoming Uttar Pradesh Assembly election, 2022. 
Adityanath Yogi is very anxious and',
            'score': 0.77364457,
            'raw_content': None
        },'''

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    return "\n----\n".join(out)      ## for all results, we can return the whole list of results as a string with separators.

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
