import sqlite3

from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print as typewriter
from qwen_agent.tools.base import BaseTool, register_tool

DB_PATH = "memories.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

@register_tool('memory_save')  # имя, под которым инструмент увидит модель
class MemorySave(BaseTool):
    # description — это по сути промпт: по нему модель решает, когда вызывать
    description = (
        'Сохраняет в долговременную память один факт о пользователе '
        '(имя, предпочтения, проекты, планы). Вызывай, когда пользователь '
        'сообщает о себе что-то, что стоит запомнить надолго.'
    )
    # parameters — JSON Schema аргументов, которые модель должна передать
    parameters = [{
        'name': 'fact',
        'type': 'string',
        'description': 'Короткий самодостаточный факт, например: «Пользователь живёт в Брно»',
        'required': True,
    }]
 
    def call(self, params: str, **kwargs) -> str:
        # params приходит строкой с JSON; этот метод BaseTool превращает её в dict
        args = self._verify_json_format_args(params)
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('INSERT INTO memories (text) VALUES (?)', (args['fact'],))
        return 'Факт сохранён.'  # эту строку увидит модель как результат вызова
 

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
 

init_db()   
llm_cfg = {
    'model': "qwen3:14b",
    'model_server': 'http://100.72.34.69:11434/v1',
    'api_key': 'ollama',
    'generate_cfg': {
        'fncall_prompt_type': 'nous',
    },
}

SYSTEM_MESSAGE = """Ты помощник с долговременной памятью. Отвечай по-русски.
- Если пользователь рассказывает о себе что-то важное, вызови memory_save.
- Если вопрос касается пользователя или прошлого, сначала вызови memory_search.
- Сохраняй по одному факту за вызов."""

messages = []
bot = Assistant(
    llm=llm_cfg,
    system_message=SYSTEM_MESSAGE,
    function_list=["memory_save", "memory_search"],
                )


while True:
    prompt = str(input("Please enter your prompt: "))

    if prompt.lower().strip() in ["exit", "quit"]:
        print("Workflow terminated by user. Exiting...")
        break

    if not prompt:
        continue

    print("Агент думает и действует:\n" + "-"*30)

    messages.append({'role': 'user', 'content': prompt})
    response_plain_text = ""
    last_response = []

    for response in bot.run(messages=messages):
        response_plain_text = typewriter(response, response_plain_text)
        last_response = response


    if last_response:
        messages.extend(last_response)
        

    print("\n" + "-"*30)

print("\n" + "-"*30)
print("Готово! Полный цикл завершен.")