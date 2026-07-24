import streamlit as st
from gigachatapi import get_access_token, send_prompt, generate_image
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

local_css("style.css")  # Создайте файл style.css в той же директории

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
        sleep(1)  # Для плавности анимации

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
    """
    Анимирует отображение сообщения в интерфейсе чата с эффектом постепенного появления текста.
    
    Функция разбивает входное сообщение на слова и отображает их последовательно с паузой,
    имитируя эффект набора текста. Стиль и скорость анимации зависят от роли отправителя:
    - Сообщения от 'user' отображаются быстрее (пауза 0.05с) с уникальным стилем
    - Сообщения от 'assistant' отображаются медленнее (пауза 0.03с) с альтернативным стилем
    
    Параметры:
        message (str): Полный текст сообщения для анимации
        role (str): Роль отправителя ("user" или "assistant"), определяющая стиль и скорость анимации
    
    Возвращает:
        str: Полностью сформированный текст сообщения после завершения анимации
    
    Использует методы Streamlit empty() и markdown() для динамического обновления контента.
    Зависит от предопределенных CSS-классов (.user-message, .assistant-message, .message-content)
    для реализации стилей.
    """
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
            
            # Если есть изображение - отображаем его
            if "image" in message:
                st.image(message["image"], use_container_width=True)

# Обработка ввода пользователя с улучшенным UI
if prompt := st.chat_input("Введите ваш вопрос..."):
    # Анимация ввода пользователя
    user_message = animate_message(prompt, "user")
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Определяем, хочет ли пользователь сгенерировать изображение
    generate_image_flag = any(keyword in prompt.lower() for keyword in ["нарисуй", "изображение", "картинку", "сгенерируй"])
    
    if generate_image_flag:
        # Анимация "генерирую изображение..."
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
        # Обычный текстовый запрос
        typing_emojis = ["✍️", "💭", "🧠", "🤔", "⌨️"]
        with st.spinner(f"{random.choice(typing_emojis)} Обрабатываю ваш запрос..."):
            response = send_prompt(prompt, st.session_state.access_token)
            
            # Анимация ответа
            assistant_message = animate_message(response, "assistant")
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})