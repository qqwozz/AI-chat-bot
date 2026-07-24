from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import streamlit as st
from gigachatapi import get_access_token, send_prompt_stream, generate_image, is_image_request, AVAILABLE_MODELS, MAX_CONTEXT_TOKENS
from time import sleep

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MAX_MESSAGE_LENGTH = 2000

# Настройка страницы
st.set_page_config(
    page_title="AI Assistant",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили CSS
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
    st.session_state.messages = [{"role": "assistant", "content": "Привет! Я ваш AI помощник. Чем могу помочь сегодня?"}]

# Заголовок
st.markdown("""
    <div class="header">
        <h1>AI Assistant</h1>
        <p>GigaChat-powered chatbot</p>
    </div>
""", unsafe_allow_html=True)

# Получение токена
if "access_token" not in st.session_state:
    with st.spinner("Connecting..."):
        st.session_state.access_token = get_access_token()
        if not st.session_state.access_token:
            st.error("Failed to get access token. Check your .env settings.")
            st.stop()

# Подсчёт токенов
def estimate_tokens(messages: list[dict]) -> int:
    total_chars = sum(len(m.get("content", "")) for m in messages if isinstance(m.get("content"), str))
    return total_chars // 4

# Боковая панель
with st.sidebar:
    st.markdown("## Settings")

    # Выбор модели
    selected_model = st.selectbox("Model", AVAILABLE_MODELS, index=0)
    st.session_state.selected_model = selected_model

    st.markdown("---")

    # Тёмная тема
    dark_mode = st.toggle("Dark mode", value=False)
    st.session_state.dark_mode = dark_mode

    st.markdown("---")

    # Счётчик токенов
    tokens_used = estimate_tokens(st.session_state.messages)
    st.metric("Tokens used", f"{tokens_used}", f"/ {MAX_CONTEXT_TOKENS} limit")

    st.markdown("---")

    # Очистка чата
    if st.button("Clear chat"):
        st.session_state.messages = [{"role": "assistant", "content": "Chat cleared. How can I help?"}]
        st.rerun()

    # Экспорт чата
    if st.button("Export chat"):
        lines = ["# Chat Export\n"]
        lines.append(f"_Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n")
        for msg in st.session_state.messages:
            role = "You" if msg["role"] == "user" else "Assistant"
            content = msg.get("content", "")
            if isinstance(content, str):
                lines.append(f"### {role}\n{content}\n")
        md_content = "\n".join(lines)
        st.download_button(
            label="Download .md",
            data=md_content,
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )

# Контейнер для чата
chat_container = st.container()

# Анимация сообщения пользователя
def animate_user_message(message: str) -> str:
    with chat_container:
        placeholder = st.empty()
        full = ""
        for word in message.split():
            full += word + " "
            sleep(0.03)
            placeholder.markdown(f"""
            <div class="user-message">
                <div class="message-content">{full}</div>
            </div>
            """, unsafe_allow_html=True)
        return full


# Отображение истории
with chat_container:
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="assistant-message">
                <div class="message-content">{message["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

            # Кнопка копирования
            if message["content"] and message["content"] != "Chat cleared. How can I help?":
                st.code(message["content"], language=None)

            if "image" in message:
                st.image(message["image"], use_container_width=True)

# Ввод пользователя
if prompt := st.chat_input("Ask me anything..."):
    if len(prompt) > MAX_MESSAGE_LENGTH:
        st.warning(f"Message too long ({len(prompt)} chars). Max: {MAX_MESSAGE_LENGTH}.")
        st.stop()

    user_message = animate_user_message(prompt)
    st.session_state.messages.append({"role": "user", "content": user_message})

    if is_image_request(prompt):
        with st.spinner("Generating image..."):
            model = st.session_state.get("selected_model", "GigaChat")
            image = generate_image(prompt, st.session_state.access_token, model)

            if image:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Here is your image: '{prompt}'",
                    "image": image
                })
                with chat_container:
                    st.image(image, caption=f"Image: '{prompt}'")
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Failed to generate image."
                })
    else:
        api_messages = [
            {"role": "system", "content": "You are a helpful AI assistant. Answer in the same language as the user."}
        ]
        for msg in st.session_state.messages:
            if msg["role"] in ("user", "assistant") and isinstance(msg.get("content"), str):
                api_messages.append({"role": msg["role"], "content": msg["content"]})

        model = st.session_state.get("selected_model", "GigaChat")

        with chat_container:
            placeholder = st.empty()
            full_response = ""
            try:
                for chunk in send_prompt_stream(api_messages, st.session_state.access_token, model):
                    full_response += chunk
                    placeholder.markdown(f"""
                    <div class="assistant-message">
                        <div class="message-content">{full_response}</div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                logger.error("Streaming error: %s", e)
                full_response = "Error processing request."

            st.session_state.messages.append({"role": "assistant", "content": full_response})
