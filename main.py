import os

import tools  # noqa: F401  (нужен ради регистрации инструментов)
from db import init_db
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print as typewriter
import dotenv
dotenv.load_dotenv()

EXIT_WORDS = {'exit', 'quit'}

llm_cfg = {
    'model': 'nvidia/nemotron-3-ultra-550b-a55b:free',
    'model_server': 'https://openrouter.ai/api/v1',
    'api_key': os.getenv('OPENROUTER_API_KEY'),
    'generate_cfg': {'fncall_prompt_type': 'nous'},
}

"""
llm_cfg = {
    'model': 'qwen3:14b',
    'model_server': 'http://100.72.34.69:11434/v1',
    'api_key': 'ollama',
    'generate_cfg': {'fncall_prompt_type': 'nous'},
}
"""

SYSTEM_MESSAGE = """Ты помощник с долговременной памятью. Отвечай по-русски.
- Если пользователь рассказывает о себе что-то важное, вызови memory_save.
- Если вопрос касается пользователя или прошлого, сначала вызови memory_search.
- Сохраняй по одному факту за вызов."""


def run_turn(bot, messages, user_text):
    """Один ход диалога: реплика пользователя -> (агентный цикл внутри bot.run) -> ответ."""
    messages.append({'role': 'user', 'content': user_text})
    printed = ''
    new_messages = []

    try:
        for new_messages in bot.run(messages=messages):
            printed = typewriter(new_messages, printed)
    except Exception as e:
        # Например, Ollama недоступна. Откатываем реплику, чтобы история
        # не осталась в «подвешенном» состоянии без ответа.
        messages.pop()
        print(f'\n[Ошибка: {e}]')
        return

    messages.extend(new_messages)


def main():
    init_db()
    bot = Assistant(
        llm=llm_cfg,
        system_message=SYSTEM_MESSAGE,
                function_list=['memory_save', 'memory_search', 'my_web_search'],
    )
    messages = []

    while True:  # внешний цикл: диалог с человеком
        try:
            prompt = input('You> ').strip()
        except (EOFError, KeyboardInterrupt):  # Ctrl+D / Ctrl+C
            print()
            break

        if prompt.lower() in EXIT_WORDS:
            break
        if not prompt:
            continue

        print('-' * 30)
        run_turn(bot, messages, prompt)
        print('\n' + '-' * 30)

    print('Готово.')


if __name__ == '__main__':
    main()