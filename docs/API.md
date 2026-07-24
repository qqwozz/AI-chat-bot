# API Reference

## gigachatapi.py

### `get_access_token() -> Optional[str]`

Получает OAuth-токен для GigaChat API.

**Возвращает:** строку с токеном или `None` при ошибке.

**Использование:**
```python
from gigachatapi import get_access_token

token = get_access_token()
if token:
    print(f"Токен получен: {token[:10]}...")
```

---

### `send_prompt(messages: list[dict], access_token: str) -> Optional[str | Image.Image]`

Отправляет список сообщений в GigaChat API.

**Параметры:**
| Параметр | Тип | Описание |
|----------|-----|----------|
| `messages` | `list[dict]` | История диалога `[{"role": "user", "content": "..."}]` |
| `access_token` | `str` | OAuth-токен |

**Возвращает:** текст ответа (`str`), изображение (`PIL.Image`) или `None`.

**Пример:**
```python
from gigachatapi import send_prompt

messages = [
    {"role": "system", "content": "Ты полезный ассистент."},
    {"role": "user", "content": "Что такое Python?"},
]
response = send_prompt(messages, token)
print(response)
```

---

### `generate_image(prompt: str, access_token: str) -> Optional[Image.Image]`

Генерирует изображение по текстовому описанию.

**Параметры:**
| Параметр | Тип | Описание |
|----------|-----|----------|
| `prompt` | `str` | Описание изображения |
| `access_token` | `str` | OAuth-токен |

**Возвращает:** `PIL.Image` или `None`.

**Пример:**
```python
from gigachatapi import generate_image

image = generate_image("кот на луне", token)
if image:
    image.save("cat_on_moon.png")
```

---

### `is_image_request(prompt: str) -> bool`

Проверяет, содержит ли запрос ключевые слова для генерации изображения.

**Ключевые слова:** `нарисуй`, `изображение`, `картинк`, `нарисуйте`, `сгенерируй`

**Пример:**
```python
from gigachatapi import is_image_request

is_image_request("нарисуй кота")   # True
is_image_request("привет")         # False
```

---

## Переменные окружения

| Переменная | Обязательна | Описание | По умолчанию |
|-----------|-------------|----------|--------------|
| `GIGACHAT_CLIENT_ID` | Да | Client ID от GigaChat | — |
| `GIGACHAT_SECRET` | Да | Secret ключ | — |
| `GIGACHAT_VERIFY_SSL` | Нет | SSL-верификация | `true` |

---

## Константы

| Константа | Значение | Описание |
|-----------|----------|----------|
| `MAX_CONTEXT_TOKENS` | 4000 | Максимум токенов в контексте |
| `CHARS_PER_TOKEN` | 4 | Символов на токен (приблизительно) |
| `MAX_RETRIES` | 3 | Максимальное число повторных попыток |
| `BASE_DELAY` | 1.0 | Базовая задержка между попытками (сек) |
