import sqlite3

from qwen_agent.tools.base import BaseTool, register_tool

from db import DB_PATH

print(DB_PATH)

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
 