import os
import logging
import requests
import uuid
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image

logger = logging.getLogger(__name__)

# Настройки API — читаются из переменных окружения
CLIENT_ID = os.environ.get("GIGACHAT_CLIENT_ID", "")
SECRET = os.environ.get("GIGACHAT_SECRET", "")
GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1"
VERIFY_SSL = os.environ.get("GIGACHAT_VERIFY_SSL", "true").lower() == "true"

# Максимальное количество токенов для контекста (~4 символа на токен)
MAX_CONTEXT_TOKENS = 4000
CHARS_PER_TOKEN = 4

IMAGE_KEYWORDS = ["нарисуй", "изображение", "картинк", "нарисуйте", "сгенерируй"]


def _trim_messages(messages: list[dict]) -> list[dict]:
    """Обрезает историю сообщений, чтобы влезть в лимит токенов."""
    total_chars = 0
    result = []
    for msg in reversed(messages):
        msg_chars = len(msg.get("content", "")) if isinstance(msg.get("content"), str) else 0
        if total_chars + msg_chars > MAX_CONTEXT_TOKENS * CHARS_PER_TOKEN:
            break
        total_chars += msg_chars
        result.append(msg)
    result.reverse()
    return result


def get_access_token():
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4())
    }
    data = {"scope": "GIGACHAT_API_PERS"}
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET.split(':')[1])
    try:
        response = requests.post(url, headers=headers, data=data, auth=auth, verify=VERIFY_SSL)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        logger.error("Ошибка при получении токена: %s", e)
        return None


def generate_image(prompt: str, access_token: str):
    url = f"{GIGACHAT_API_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "GigaChat",
        "messages": [
            {"role": "system", "content": "Ты — художник, который создает изображения по описанию."},
            {"role": "user", "content": prompt}
        ],
        "function_call": "auto"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=VERIFY_SSL)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        soup = BeautifulSoup(content, "html.parser")
        img_tag = soup.find("img")
        if not img_tag:
            return None

        file_id = img_tag["src"]
        image_url = f"{GIGACHAT_API_URL}/files/{file_id}/content"
        image_response = requests.get(image_url, headers=headers, verify=VERIFY_SSL)
        image_response.raise_for_status()

        return Image.open(BytesIO(image_response.content))
    except Exception as e:
        logger.error("Ошибка при генерации изображения: %s", e)
        return None


def is_image_request(prompt: str) -> bool:
    """Проверяет, содержит ли запрос ключевые слова для генерации изображения."""
    return any(word in prompt.lower() for word in IMAGE_KEYWORDS)


def send_prompt(messages: list[dict], access_token: str):
    """
    Отправляет список сообщений в GigaChat API с ограничением контекста.

    messages: [{"role": "user"/"assistant", "content": "..."}]
    Возвращает ответ модели (str) или None при ошибке.
    """
    if messages and is_image_request(messages[-1].get("content", "")):
        return generate_image(messages[-1]["content"], access_token)

    trimmed = _trim_messages(messages)

    url = f"{GIGACHAT_API_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "GigaChat",
        "messages": trimmed,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, verify=VERIFY_SSL)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error("Ошибка при запросе к GigaChat: %s", e)
        return None
