from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("web_search_api_key"))
response = tavily_client.search("Who is Leo Messi?")

print(response)