from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from datetime import datetime
import os
from blogsmith.env import NEWSDATA_IO_API_KEY
from typing import List, TypedDict , Dict
import json
from functools import lru_cache

from tenacity import retry, wait_exponential, stop_after_attempt
import httpx
import requests_cache


# utils api function for caching and retrying the api call

#storing the cache in the local directory so that it can be used in the future runs
requests_cache.install_cache("news_cache", expire_after=1800)

@lru_cache(maxsize=128)
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(4))
def getNewsByToken(token: str, categories: str) -> List[Dict]:
    max_articles = 3
    base_url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWSDATA_IO_API_KEY,
        "q": token,
        "category":categories,
        "language": "en"
    }
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(base_url, params=params)
            response.raise_for_status()
            return response.json().get("results", [])[:max_articles]
    except httpx.RequestError as e:
        raise Exception(f"HTTP error while requesting news data: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")


@lru_cache(maxsize=128)
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def getWordsByToken(token: str) -> list:
    url = f"https://api.datamuse.com/words?{token}&max=4"

    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(url)
            response.raise_for_status()  # Raises error if not 200
            return response.json()
    except httpx.HTTPStatusError as e:
        raise Exception(f"Non-200 response from Datamuse API: {e}")
    except httpx.RequestError as e:
        raise Exception(f"Request error while reaching Datamuse API: {e}")


# tool for saving the content of the blog in markdown and metadata in json format

class SaveFileToolInput(BaseModel):
    """Input schema for SaveFileTool."""
    content: str = Field(..., description="Content of blog to save in file in markdown format")
    metadata: str = Field(..., description="Metadata of blog for SEO ((title, description, keywords, slug ,etc) in json format")

class SaveFileTool(BaseTool):
    name: str = "File saving tool"
    description: str = (
        "Saves the content of the blog in markdown and metadata in json format."
    )
    args_schema: Type[BaseModel] = SaveFileToolInput
    def _run(self, content: str, metadata: str) -> str:
        parse_metadata = json.loads(metadata)
        filename = datetime.now().timestamp()
        if(parse_metadata.get("slug") != None):
            filename= parse_metadata.get("slug")
        markdown_file = f"output/{filename}_blog.md"
        json_file = f"output/{filename}_metadata.json"
        try: 
            os.makedirs("output", exist_ok=True)

            with open(markdown_file, "w") as f:
                f.write(content)
            with open(json_file, "w") as f:
                f.write(metadata)  
        except Exception as e:
            raise Exception(f"An error occurred while saving the files: {e}")
        return "File saving is process is done"

# tool for searching new regrading the topic and context 

class NewsArticle(TypedDict):
    title: str
    link: str
    description: str
    pubDate: str
    source: str

class SearchNewsToolInput(BaseModel):
    """Input schema for Search News."""
    tokens: List[str] = Field(..., description="top 4 words or title for searching based on topic")
    categories : List[str] = Field(... , description="at max 4 category of the news to be searched based on the tone of the blog only including {business,crime,domestic,education,entertainment,environment,food,health,lifestyle,other,politics,science,sports,technology,tourism,world}")
  
class SearchNewsTool(BaseTool):
    name: str = "Search News"
    description: str = (
        "Searches for the latest news articles based on the given tokens."
        "Returns a parsed list of articles with title, link, description, publication date, and source."
    )
    args_schema: Type[BaseModel] = SearchNewsToolInput

    def _run(self, tokens: List[str] , categories : List[str]) -> List[NewsArticle]:
        parsed : List[NewsArticle]= []
        for token in tokens[:4]:
            categories.sort()
            results = getNewsByToken(token  ,  f"top,{",".join(categories[:4])}")
            for article in results:
                parsed.append({
                    "title": article.get("title"),
                    "link": article.get("link"),
                    "description": article.get("description"),
                    "pubDate": article.get("pubDate"),
                    "source": article.get("source_name")
                })
        return parsed
    
class WordSearchingToolInput(BaseModel):
    """Input schema for Word Searching Tool."""
    tokens : List[str] = Field(..., description="10 tokens for searching the words for the blog based on the topic and tone")

class WordSearchingTool(BaseTool):
    name: str = "Word Searching Tool"
    description: str = (
        "Searches for the words based on the topic and tone of the blog."
        "for words with a meaning similar to ringing in the ears give input token like ml=ringing+in+the+ears"
        "words that sound like jirraf give input token like sl=jirraf"
        "words that are spelled similarly to hipopatamus give input token like sp=hipopatamus"
        "words that are triggered by (strongly associated with) the word \"cow\" give input token like rel_trg=cow"
        "Return a parsed list of words."
    )
    args_schema: Type[BaseModel] = WordSearchingToolInput

    def _run(self, tokens: List[str]) -> List[str]:
        words : List[str] = []
        for token in tokens[:10]:
            response = getWordsByToken(token)  
            for iter in response:
                word = iter.get("word")
                words.append(word)
        return words