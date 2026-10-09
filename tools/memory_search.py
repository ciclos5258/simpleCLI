import sqlite3


from qwen_agent.tools.base import BaseTool, register_tool

@register_tool('memory_search')
class MemorySearch(BaseTool):
    description = (
        'Ищет в долговременной памяти факты о пользователе. '
        'Вызывай, когда вопрос касается самого пользователя или прошлых разговоров. '
        'Пустой запрос вернёт все сохранённые факты.'
    )
    parameters = [{
        'name': 'query',
        'type': 'string',
        'description': 'Ключевые слова для поиска (или пустая строка)',
        'required': True,
    }]
 
    def call(self, params: str, **kwargs) -> str:
        query = self._verify_json_format_args(params)['query'].lower()
 
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute('SELECT text FROM memories').fetchall()
 
        # Фильтруем в Python, а не через SQL LIKE: LIKE в SQLite не учитывает
        # регистр только для латиницы, а для кириллицы «Брно» != «брно».
        words = query.split()
        found = [
            text for (text,) in rows
            if not words or any(w in text.lower() for w in words)
        ]
 
        if not found:
            return 'В памяти ничего не найдено.'
        return '\n'.join(f'- {t}' for t in found)
 