from openai import OpenAI

client = OpenAI(
    base_url = "http://100.72.34.69:11434/v1",
    api_key = "ollama"
)

prompt = str(input("Hello!"))

stream = client.chat.completions.create(
    model="qwen3:14b",
    messages=[{"role": "user", "content": prompt},],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choises[0].delta.content, end="", flush=True)

print()