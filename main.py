import tools

from db import init_db
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print as typewriter


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