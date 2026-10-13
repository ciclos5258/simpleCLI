import os

from qwen_agent.tools.base import BaseTool, register_tool
from tavily import TavilyClient

from datetime import date
from dotenv import load_dotenv
load_dotenv()

@register_tool('web_search')
class WebSearch(BaseTool):
    current_date = str(date.today())
    description = (
        'Делает запрос в интернет и возвращает результаты поиска.'
        'Вызывай, когда тебе нужны актуальные данные из интернета.'
    )
    # parameters — JSON Schema аргументов, которые модель должна передать
    parameters = [{
        'name': 'query',
        'type': 'string',
        'description': (
            f'Поисковый запрос (ключевые слова). '
            f'Например: «новости за {current_date}», «погода в Брно», '
            f'«выручка Яндекса в 2024 году».'
        ),
        'required': True,
    }]

    def call(self, params: str, **kwargs) -> str:
        current_date = str(date.today())

        args = self._verify_json_format_args(params)
        query = args['query']

        search_engine = TavilyClient(api_key=os.getenv('web_search_api_key'))
        raw_search = search_engine.search(query=query)

        results = raw_search.get('results', [])
        if not results:
            return 'По запросу ничего не найдено.'

        snippets = []
        for r in results:
            title = r.get('title', 'Без заголовка')
            url = r.get('url', '')
            content = r.get('content', '')
            published_date = r.get('published_date') or r.get('publishing_date', '')

            snippet = f'🔹 **{title}**\n{content}'
            if published_date:
                snippet += f'\n📅 {published_date}'
            if url:
                snippet += f'\n🔗 {url}'
            snippets.append(snippet)

        return f'Сегодня: {current_date}\n\n' + '\n\n'.join(snippets)
