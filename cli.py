from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter

llm_cfg = {
    'model': "qwen3:14b",
    'model_server': 'http://100.72.34.69:11434/v1',
    'api_key': 'ollama',
    'generate_cfg': {
        'fncall_prompt_type': 'nous',
    },
}

bot = Assistant(llm_cfg=llm_cfg)

prompt = str(input("Please enter your prompt: "))

messages = [{'role': 'user', 'content': prompt}]

print("Агент думает и действует:\n" + "-"*30)

response_plain_text = ""

for response in bot.run(messages=messages):
    response_plain_text = typewriter(response, response_plain_text)

print("\n" + "-"*30)
print("Готово! Полный цикл завершен.")