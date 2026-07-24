<div align="center">

# 🤖 GigaChat AI Assistant

**Интерактивный чат-бот с мульти-диалогом, streaming-ответами и генерацией изображений**

[![CI](https://github.com/qqwozz/AI-chat-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/qqwozz/AI-chat-bot/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Документация](docs/ARCHITECTURE.md) | [API Reference](docs/API.md) | [Установка](docs/SETUP.md)

</div>

---

## ✨ Возможности

<table>
<tr>
<td width="50%">

### 🧠 Умный диалог
- Мульти-контекст — бот помнит историю (до 4000 токенов)
- Streaming — текст появляется по мере генерации
- Выбор модели: GigaChat / Pro / Lite

</td>
<td width="50%">

### 🎨 Генерация изображений
- По текстовому описанию
- Автоопределение запроса по ключевым словам
- Отображение прямо в чате

</td>
</tr>
<tr>
<td>

### 🛡️ Надёжность
- Retry с экспоненциальной задержкой (3 попытки)
- SSL-верификация (настраивается)
- Логирование всех ошибок

</td>
<td>

### 🎨 UX
- Тёмная / светлая тема
- Анимация набора текста
- Экспорт чата в Markdown
- Адаптивный дизайн

</td>
</tr>
</table>

---

## 🚀 Быстрый старт

```bash
# 1. Клонировать
git clone https://github.com/qqwozz/AI-chat-bot.git
cd AI-chat-bot

# 2. Установить зависимости
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Настроить
cp .env.example .env
# Заполнить .env ключами GigaChat (см. docs/SETUP.md)

# 4. Запустить
streamlit run main.py
```

> Приложение откроется на `http://localhost:8501`

---

## 🏗 Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                      Пользователь                       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   Streamlit UI (main.py)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │  Чат     │ │  Тема    │ │  Модель  │ │  Экспорт  │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              API-клиент (gigachatapi.py)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │  Auth    │ │  Retry   │ │ Stream   │ │  Context  │  │
│  │  OAuth   │ │  3 tries │ │  SSE     │ │  4000 tok │  │
│  └──────────┘ └──────────┘ └──────────┘ └───────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   GigaChat API (Сбербанк)               │
└─────────────────────────────────────────────────────────┘
```

Подробнее: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📁 Структура проекта

```
AI-chat-bot/
├── main.py                    # Streamlit UI + streaming
├── gigachatapi.py             # API-клиент (auth, retry, SSE, context)
├── style.css                  # Стили (светлая + тёмная тема)
├── requirements.txt           # Зависимости
├── .env.example               # Шаблон переменных окружения
├── Dockerfile                 # Docker-образ
├── docker-compose.yml         # Docker Compose
│
├── tests/
│   └── test_gigachatapi.py    # Unit-тесты (pytest)
│
├── docs/
│   ├── ARCHITECTURE.md        # Архитектура и потоки данных
│   ├── API.md                 # Справочник по API
│   ├── SETUP.md               # Установка и запуск
│   └── CONTRIBUTING.md        # Участие в разработке
│
└── .github/workflows/
    └── ci.yml                 # GitHub Actions CI
```

---

## 🛠 Технологии

| Слой | Технология | Зачем |
|------|-----------|-------|
| **Язык** | Python 3.10+ | Type hints, совместимость |
| **UI** | Streamlit | Быстрый прототипинг веб-интерфейсов |
| **AI** | GigaChat API | NLP + генерация изображений |
| **Тесты** | pytest | Unit-тесты с моками |
| **CI/CD** | GitHub Actions | Автоматические тесты при пуше |
| **Контейнеры** | Docker | Воспроизводимый деплой |

---

## 💻 Использование API

```python
from gigachatapi import get_access_token, send_prompt, send_prompt_stream

# Получить токен
token = get_access_token()

# Обычный запрос
response = send_prompt(
    [{"role": "user", "content": "Что такое Python?"}],
    token,
    model="GigaChat"
)

# Streaming-запрос (текст по мере генерации)
for chunk in send_prompt_stream(
    [{"role": "user", "content": "Расскажи анекдот"}],
    token,
    model="GigaChat-Pro"
):
    print(chunk, end="", flush=True)
```

Подробнее: [docs/API.md](docs/API.md)

---

## 🧪 Тесты

```bash
pytest tests/ -v
```

```
tests/test_gigachatapi.py::TestTrimMessages::test_empty_list       PASSED
tests/test_gigachatapi.py::TestTrimMessages::test_long_history      PASSED
tests/test_gigachatapi.py::TestIsImageRequest::test_naarissuj      PASSED
tests/test_gigachatapi.py::TestGetAccessToken::test_success        PASSED
tests/test_gigachatapi.py::TestSendPrompt::test_text_request       PASSED
tests/test_gigachatapi.py::TestSendPrompt::test_image_delegates    PASSED
───────────────────────────────────────────────────────────────────
6 passed in 0.12s
```

---

## 🐳 Docker

```bash
# Через Docker Compose (рекомендуется)
docker compose up --build

# Или вручную
docker build -t gigachat-bot .
docker run -p 8501:8501 --env-file .env gigachat-bot
```

> Приложение: `http://localhost:8501`

---

## ⚙️ Переменные окружения

| Переменная | Обязательна | Описание | По умолчанию |
|-----------|-------------|----------|--------------|
| `GIGACHAT_CLIENT_ID` | ✅ | Client ID от GigaChat | — |
| `GIGACHAT_SECRET` | ✅ | Secret ключ | — |
| `GIGACHAT_VERIFY_SSL` | ❌ | SSL-верификация | `true` |

---

## 📄 Документация

| Документ | Описание |
|----------|----------|
| [Архитектура](docs/ARCHITECTURE.md) | Схема потоков данных, retry-логика, контекст |
| [API Reference](docs/API.md) | Все функции, параметры, примеры |
| [Установка](docs/SETUP.md) | Пошаговая инструкция, Docker, ключи |
| [Участие](docs/CONTRIBUTING.md) | Чек-лист, формат коммитов |

---

## 👤 Контакты

<div align="center">

[![Email](https://img.shields.io/badge/Email-offconix%40gmail.com-blue)](mailto:offconix@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-@onixxed-26A5E4)](https://t.me/onixxed)
[![GitHub](https://img.shields.io/badge/GitHub-qqwozz-181717)](https://github.com/qqwozz)

</div>

---

<div align="center">

Сделано с ❤️ для вас

</div>
