# GigaChat AI Assistant

Интерактивный чат-бот с мульти-диалогом и генерацией изображений на базе GigaChat API от Сбербанка.

## Демо

```
Пользователь: Привет! Расскажи про Python
Бот:          Python — это язык программирования высокого уровня...

Пользователь: А теперь нарисуй кота на луне
Бот:          [изображение]
```

## Возможности

- **Мульти-диалог** — бот помнит контекст разговора (до 4000 токенов)
- **Генерация изображений** — по текстовому описанию через GigaChat
- **Retry с backoff** — автоматические повторы при ошибках сервера
- **Анимация текста** — эффект набора сообщения
- **Адаптивный дизайн** — работает на мобильных устройствах

## Быстрый старт

```bash
# Клонировать
git clone https://github.com/qqwozz/AI-chat-bot.git
cd AI-chat-bot

# Установить зависимости
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Настроить
cp .env.example .env
# Заполнить .env своими ключами GigaChat

# Запустить
streamlit run main.py
```

Подробнее: [docs/SETUP.md](docs/SETUP.md)

## Структура проекта

```
AI-chat-bot/
├── main.py                 # Streamlit UI
├── gigachatapi.py          # API-клиент (auth, retry, context)
├── style.css               # Стили чата
├── requirements.txt        # Зависимости
├── .env.example            # Шаблон переменных окружения
├── .gitignore
├── Dockerfile              # Docker-образ
├── docker-compose.yml      # Docker Compose
├── tests/
│   └── test_gigachatapi.py # Unit-тесты (pytest)
├── docs/
│   ├── ARCHITECTURE.md     # Архитектура и потоки данных
│   ├── API.md              # Справочник по API
│   ├── SETUP.md            # Установка и запуск
│   └── CONTRIBUTING.md     # Участие в разработке
└── .github/workflows/
    └── ci.yml              # GitHub Actions CI
```

## Технологии

| Компонент | Технология |
|-----------|-----------|
| Язык | Python 3.10+ |
| UI | Streamlit |
| AI-модель | GigaChat (Сбербанк) |
| Тесты | pytest |
| CI/CD | GitHub Actions |
| Контейнеризация | Docker |

## Как это работает

```
Пользователь ──▶ Streamlit UI ──▶ gigachatapi.py ──▶ GigaChat API
                    │                    │
                    │                    ├── OAuth-аутентификация
                    │                    ├── Retry (3 попытки, backoff)
                    │                    └── Обрезка контекста (4000 токенов)
                    │
                    └── Анимация текста + CSS-стили
```

Подробнее: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## API

```python
from gigachatapi import get_access_token, send_prompt

token = get_access_token()
response = send_prompt(
    [{"role": "user", "content": "Привет!"}],
    token
)
print(response)  # "Здравствуйте! Чем могу помочь?"
```

Подробнее: [docs/API.md](docs/API.md)

## Тесты

```bash
pytest tests/ -v
```

```
tests/test_gigachatapi.py::TestTrimMessages::test_empty_list PASSED
tests/test_gigachatapi.py::TestIsImageRequest::test_naarissuj PASSED
tests/test_gigachatapi.py::TestGetAccessToken::test_success PASSED
tests/test_gigachatapi.py::TestSendPrompt::test_text_request PASSED
...
```

## Docker

```bash
docker compose up --build
# Приложение доступно на http://localhost:8501
```

## Контакты

- Email: offconix@gmail.com
- Telegram: @onixxed
- GitHub: [qqwozz](https://github.com/qqwozz)
