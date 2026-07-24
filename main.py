import streamlit as st
from gigachatapi import get_access_token, send_prompt, generate_image, is_image_request
from time import sleep
import random

# Настройка страницы
st.set_page_config(
    page_title="AI Чат-бот",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Стили CSS для улучшения внешнего вида
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

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
    st.markdown("🛠️ Разработано с ❤️ для вас")

# Контейнер для чата
chat_container = st.container()

# Анимация ввода сообщения
def animate_message(message, role):
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
    user_message = animate_message(prompt, "user")
    st.session_state.messages.append({"role": "user", "content": user_message})

    if is_image_request(prompt):
        with st.spinner("🎨 Генерирую изображение..."):
            image = generate_image(prompt, st.session_state.access_token)

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

        typing_emojis = ["✍️", "💭", "🧠", "🤔", "⌨️"]
        with st.spinner(f"{random.choice(typing_emojis)} Обрабатываю ваш запрос..."):
            response = send_prompt(api_messages, st.session_state.access_token)

            if response:
                assistant_message = animate_message(response, "assistant")
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Произошла ошибка при обработке запроса"
                })
