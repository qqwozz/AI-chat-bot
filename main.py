from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import streamlit as st
from gigachatapi import get_access_token, send_prompt, send_prompt_stream, generate_image, is_image_request, AVAILABLE_MODELS
from time import sleep
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 2000

# Настройка страницы
st.set_page_config(
    page_title="AI Чат-бот",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили CSS для улучшения внешнего вида
def local_css(file_name: str) -> None:
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Применение темы через JS
def apply_theme() -> None:
    theme = "dark" if st.session_state.get("dark_mode", False) else "light"
    st.markdown(f"""
    <script>
        document.documentElement.setAttribute("data-theme", "{theme}");
    </script>
    """, unsafe_allow_html=True)

apply_theme()

# Инициализация сессии
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Привет! Я ваш AI помощник. Чем могу помочь сегодня? 😊"}]

# Красивое оформление заголовка
st.markdown("""
    <div class="header">
        <h1 style='text-align: center; color: #4a4a4a;'>
            <span style='color: #6e48aa;'>AI</span> Чат-бот
        </h1>
        <p style='text-align: center; color: #7a7a7a;'>
            Ваш интеллектуальный помощник на базе GigaChat
        </p>
    </div>
""", unsafe_allow_html=True)

# Получение токена с индикатором загрузки
if "access_token" not in st.session_state:
    with st.spinner("🔐 Устанавливаем безопасное соединение..."):
        st.session_state.access_token = get_access_token()
        if not st.session_state.access_token:
            st.error("Не удалось получить токен доступа. Проверьте настройки.")
            st.stop()
        sleep(1)

# Боковая панель с информацией
with st.sidebar:
    st.markdown("## 📌 О чат-боте")
    st.markdown("""
    Это интеллектуальный помощник на базе GigaChat API.
    Вы можете задавать любые вопросы и получать развернутые ответы.
    """)

    st.markdown("---")

    # Выбор модели
    selected_model = st.selectbox("🧠 Модель", AVAILABLE_MODELS, index=0)
    st.session_state.selected_model = selected_model

    st.markdown("---")

    # Тёмная тема
    dark_mode = st.toggle("🌙 Тёмная тема", value=False)
    st.session_state.dark_mode = dark_mode

    # Экспорт чата
    if st.button("📥 Экспорт чата в Markdown"):
        lines = ["# Чат с AI-ассистентом\n"]
        lines.append(f"_Экспортировано: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
        for msg in st.session_state.messages:
            role = "Пользователь" if msg["role"] == "user" else "Ассистент"
            content = msg.get("content", "")
            if isinstance(content, str):
                lines.append(f"### {role}\n{content}\n")
        md_content = "\n".join(lines)
        st.download_button(
            label="💾 Скачать .md файл",
            data=md_content,
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )

    st.markdown("---")
    st.markdown("🛠️ Разработано с ❤️ для вас")

# Контейнер для чата
chat_container = st.container()

# Анимация ввода сообщения
def animate_message(message: str, role: str) -> str:
    with chat_container:
        if role == "user":
            message_placeholder = st.empty()
            full_response = ""
            for chunk in message.split():
                full_response += chunk + " "
                sleep(0.05)
                message_placeholder.markdown(f"""
                <div class="user-message">
                    <div class="message-content">
                        {full_response}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            message_placeholder = st.empty()
            full_response = ""
            for chunk in message.split():
                full_response += chunk + " "
                sleep(0.03)
                message_placeholder.markdown(f"""
                <div class="assistant-message">
                    <div class="message-content">
                        {full_response}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        return full_response


# Отображение истории сообщений
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="message-content">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="message-content">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if "image" in message:
                st.image(message["image"], use_container_width=True)

# Обработка ввода пользователя
if prompt := st.chat_input("Введите ваш вопрос..."):
    if len(prompt) > MAX_MESSAGE_LENGTH:
        st.warning(f"Сообщение слишком длинное ({len(prompt)} символов). Максимум: {MAX_MESSAGE_LENGTH}.")
        st.stop()

    user_message = animate_message(prompt, "user")
    st.session_state.messages.append({"role": "user", "content": user_message})

    if is_image_request(prompt):
        with st.spinner("🎨 Генерирую изображение..."):
            model = st.session_state.get("selected_model", "GigaChat")
            image = generate_image(prompt, st.session_state.access_token, model)

            if image:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Вот изображение по вашему запросу: '{prompt}'",
                    "image": image
                })

                with chat_container:
                    st.image(image, caption=f"Изображение по запросу: '{prompt}'")
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Извините, не удалось сгенерировать изображение"
                })
    else:
        # Собираем историю для API (только текстовые сообщения)
        api_messages = [
            {"role": "system", "content": "Ты полезный AI-ассистент. Отвечай на русском языке."}
        ]
        for msg in st.session_state.messages:
            if msg["role"] in ("user", "assistant") and isinstance(msg.get("content"), str):
                api_messages.append({"role": msg["role"], "content": msg["content"]})

        model = st.session_state.get("selected_model", "GigaChat")

        # Streaming: отображаем ответ по мере генерации
        with chat_container:
            message_placeholder = st.empty()
            full_response = ""
            try:
                for chunk in send_prompt_stream(api_messages, st.session_state.access_token, model):
                    full_response += chunk
                    message_placeholder.markdown(f"""
                    <div class="assistant-message">
                        <div class="message-content">
                            {full_response}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                logger.error("Streaming error: %s", e)
                full_response = "Произошла ошибка при обработке запроса"

            st.session_state.messages.append({"role": "assistant", "content": full_response})
