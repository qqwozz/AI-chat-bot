# GigaChat AI Assistant

Интерактивный чат-бот с мульти-диалогом и генерацией изображений на базе GigaChat API.

## Возможности

- Мульти-диалог — бот помнит контекст разговора (до 4000 токенов)
- Генерация изображений по текстовому описанию
- Анимация набора текста
- Адаптивный дизайн для мобильных устройств

## Быстрый старт

### Требования

- Python 3.10+
- Аккаунт разработчика GigaChat ([регистрация](https://developers.sber.ru/))

### Установка

```bash
git clone https://github.com/qqwozz/AI-chat-bot.git
cd AI-chat-bot
pip install -r requirements.txt
```

### Настройка

Создайте файл `.env` в корне проекта:

```
GIGACHAT_CLIENT_ID=ваш_client_id
GIGACHAT_SECRET=ваш_secret
GIGACHAT_VERIFY_SSL=true
```

### Запуск

```bash
streamlit run main.py
```

### Тесты

```bash
pytest tests/ -v
```

## Структура проекта

```
AI-chat-bot/
├── main.py              # Streamlit UI
├── gigachatapi.py       # API-клиент GigaChat
├── style.css            # Стили интерфейса
├── requirements.txt     # Зависимости
├── .env.example         # Шаблон переменных окружения
├── tests/
│   └── test_gigachatapi.py
└── Dockerfile
```

## Технологии

- **Python 3.10+** — основной язык
- **Streamlit** — веб-интерфейс
- **GigaChat API** — AI-модель от Сбербанка
- **pytest** — тестирование
- **GitHub Actions** — CI/CD

## Контакты

- Email: offconix@gmail.com
- Telegram: @onixxed
- GitHub: [qqwozz](https://github.com/qqwozz)
