# Самописный агент, поддерживает OpenAI API

## Запуск

```bash
pip install qwen-agent
python main.py # запуск ИЗ КОРНЯ, иначе - ломается поведение пакетов
```

Агент общается с LLM по адресу, который лежит в llm_cfg из main.py

## План

- [x] Убрать позорный `while: True`
- [ ] Семантический поиск воспоминаний
- [ ] `memory_update` / `memory_delete`
- [x] Веб поиск
- [ ] Доступ к изолированной Bash
- [ ] Agentic loop