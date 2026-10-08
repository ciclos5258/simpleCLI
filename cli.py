from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print as typewriter

llm_cfg = {
    'model': "qwen3:14b",
    'model_server': 'http://100.72.34.69:11434/v1',
    'api_key': 'ollama',
    'generate_cfg': {
        'fncall_prompt_type': 'nous',
    },
}

messages = []
bot = Assistant(llm=llm_cfg)


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