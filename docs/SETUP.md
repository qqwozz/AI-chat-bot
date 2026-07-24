# Установка и запуск

## Требования

- Python 3.10+
- Аккаунт разработчика GigaChat ([регистрация](https://developers.sber.ru/))

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/qqwozz/AI-chat-bot.git
cd AI-chat-bot
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` в корне проекта:

```bash
cp .env.example .env
```

Заполните его:

```
GIGACHAT_CLIENT_ID=ваш_client_id
GIGACHAT_SECRET=ваш_secret
GIGACHAT_VERIFY_SSL=true
```

### 5. Запуск

```bash
streamlit run main.py
```

Приложение откроется в браузере по адресу `http://localhost:8501`.

---

## Docker

### Запуск через Docker Compose

```bash
docker compose up --build
```

### Запуск через Docker

```bash
docker build -t gigachat-bot .
docker run -p 8501:8501 --env-file .env gigachat-bot
```

---

## Тесты

```bash
pytest tests/ -v
```

---

## Получение ключей GigaChat

1. Зарегистрируйтесь на [developers.sber.ru](https://developers.sber.ru/)
2. Создайте приложение
3. Скопируйте `CLIENT_ID` и `SECRET`
4. Вставьте в `.env`

---

## Структура `.env`

```
GIGACHAT_CLIENT_ID=abc123...
GIGACHAT_SECRET=xyz789...
GIGACHAT_VERIFY_SSL=true
```

**Важно:** файл `.env` не должен попасть в git (уже добавлен в `.gitignore`).
