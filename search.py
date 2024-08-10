import functools, operator, requests, os, json
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def internet_search(query: str):
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(
            query,
            max_results=5, 
            region="wt-wt", 
            safesearch="moderate", 
            timelimit="y",
            backend="api",
        )
        if ddgs_gen:
            return [r for r in ddgs_gen]
    return "No results found."
    
def process_content(url: str, threhold:int=1000) -> list:
    """Processes content from a webpage."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Reform the text into paragraphs
    candidate_paragraphs = (paragraph.strip() for paragraph in text.split("\n"))
    paragraphs = []
    current_paragraph = ""
    
    for candidate in candidate_paragraphs:
        if len(candidate) > 0:
            if len(current_paragraph) + len(candidate) <= threhold:
                current_paragraph += candidate + " "
            else:
                while len(candidate) > threhold:
                    if len(current_paragraph) > 0:
                        paragraphs.append(current_paragraph.strip() + "\n")
                        current_paragraph = ""
                    paragraphs.append(candidate[:threhold].strip() + "\n")
                    candidate = candidate[threhold:]
                if len(current_paragraph) + len(candidate) > threhold:
                    paragraphs.append(current_paragraph.strip() + "\n")
                    current_paragraph = candidate + " "
                else:
                    current_paragraph += candidate + " "
    
    if current_paragraph:
        paragraphs.append(current_paragraph.strip() + "\n")
    
    return paragraphs