import requests
import uuid
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image

# Настройки API
CLIENT_ID = ''
SECRET = ''
GIGACHAT_API_URL = "https://gigachat.devices.sberbank.ru/api/v1"


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
        response = requests.post(url, headers=headers, data=data, auth=auth, verify=False)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        print(f"Ошибка при получении токена: {str(e)}")
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
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        soup = BeautifulSoup(content, "html.parser")
        img_tag = soup.find("img")
        if not img_tag:
            return None

        file_id = img_tag["src"]
        image_url = f"{GIGACHAT_API_URL}/files/{file_id}/content"
        image_response = requests.get(image_url, headers=headers, verify=False)
        image_response.raise_for_status()

        return Image.open(BytesIO(image_response.content))
    except Exception as e:
        print(f"Ошибка при генерации изображения: {str(e)}")
        return None


def send_prompt(prompt: str, access_token: str):
    if any(word in prompt.lower() for word in ["нарисуй", "изображение", "картинк", "нарисуйте"]):
        return generate_image(prompt, access_token)
    else:
        url = f"{GIGACHAT_API_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=payload, verify=False)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Ошибка при запросе к GigaChat: {str(e)}")
            return None
