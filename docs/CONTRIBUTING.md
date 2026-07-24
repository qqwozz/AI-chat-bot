# Участие в разработке

## Чек-лист перед коммитом

1. Тесты проходят: `pytest tests/ -v`
2. Код не содержит `print()` — используйте `logging`
3. Функции имеют type hints
4. `.env` не в коммите

## Структура коммитов

Формат: `<тип>: <описание>`

Типы:
- `feat` — новая фича
- `fix` — исправление бага
- `test` — тесты
- `docs` — документация
- `ci` — CI/CD
- `chore` — сборка, зависимости

Примеры:
```
feat: add voice input support
fix: token refresh on 401
test: add retry unit tests
docs: update API reference
```

## Запуск локально

```bash
# Установка
pip install -r requirements.txt

# Запуск
streamlit run main.py

# Тесты
pytest tests/ -v
```

## Добавление новой фичи

1. Создать ветку: `git checkout -b feat/название`
2. Написать код
3. Добавить тесты в `tests/`
4. Убедиться что `pytest tests/ -v` проходит
5. Закоммитить и запушить
6. Создать PR
