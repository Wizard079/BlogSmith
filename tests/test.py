import httpx
from blogsmith.env import NEWSDATA_IO_API_KEY
max_artical = 3
parsed = []
tokens = ['artificial intelligence', 'machine learning', 'deep learning', 'natural language processing']
categories = ['technology', 'science', 'business']
max_articles = 3
base_url = "https://newsdata.io/api/1/news"
categories.sort()
categories = f"top,{",".join(categories)}"
for token in tokens:
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
            x= response.json().get("results", [])[:max_articles]
    except httpx.RequestError as e:
        raise Exception(f"HTTP error while requesting news data: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
print(parsed)
print(x)