import os
import json
from tavily import TavilyClient

client = TavilyClient(api_key=os.getenv('web_search_api_key'))
raw = client.search(query='погода в Брно')

print(json.dumps(raw, indent=2, ensure_ascii=False))