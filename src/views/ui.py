import streamlit as st
from typing import Callable, Dict, Any
import json
from src.config.settings import (
    PAGE_TITLE,
    PAGE_ICON,
    PAGE_LAYOUT,
    AVAILABLE_MODELS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    SYSTEM_PROMPTS_FILE
)

def create_copy_button(text: str, key: str):
    """Tạo nút copy cho text"""
    if st.button("📋 Copy", key=f"copy_{key}"):
        st.write("Đã copy!")
        st.session_state["copied_text"] = text

def create_reset_button(message_index: int, on_reset: Callable):
    """Tạo nút reset cho message"""
    if st.button("🔄 Reset", key=f"reset_{message_index}"):
        on_reset(message_index)

def create_chat_ui(chat_instance: Any):
    """Tạo giao diện chat chính"""
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=PAGE_LAYOUT
    )

    # Header
    st.title("🤖 Mr. Lễ AI")
    st.markdown("Chương trình được tạo bởi Mr. Lễ AI - Với sự hỗ trợ của ClaudeAI")

    # Sidebar cho cài đặt và quản lý system prompts
    with st.sidebar:
        st.header("⚙️ Cài đặt")
        
        # Quản lý System Prompts
        st.subheader("🤖 Quản lý Chatbots")
        
        # Đọc system prompts từ file
        try:
            with open(SYSTEM_PROMPTS_FILE, 'r', encoding='utf-8') as f:
                system_prompts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            system_prompts = {
                "Default": "You are Mr. 'Lễ đẹp trai' a helpful AI assistant. Respond in Vietnamese."
            }

        # Chọn chatbot
        selected_bot = st.selectbox(
            "Chọn Chatbot",
            options=list(system_prompts.keys()),
            key="selected_bot"
        )

        # Hiển thị và chỉnh sửa system prompt
        current_prompt = st.text_area(
            "System Prompt",
            value=system_prompts[selected_bot],
            height=100,
            key="current_prompt"
        )

        # Nút lưu thay đổi
        if st.button("💾 Lưu thay đổi"):
            system_prompts[selected_bot] = current_prompt
            with open(SYSTEM_PROMPTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(system_prompts, f, ensure_ascii=False, indent=2)
            st.success("Đã lưu thay đổi!")

        # Tạo chatbot mới
        st.subheader("➕ Tạo Chatbot mới")
        new_bot_name = st.text_input("Tên Chatbot mới")
        new_bot_prompt = st.text_area("System Prompt mới", height=100)
        
        if st.button("Tạo mới") and new_bot_name and new_bot_prompt:
            system_prompts[new_bot_name] = new_bot_prompt
            with open(SYSTEM_PROMPTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(system_prompts, f, ensure_ascii=False, indent=2)
            st.success(f"Đã tạo chatbot mới: {new_bot_name}")
            st.experimental_rerun()

        # Các cài đặt khác
        st.subheader("🛠️ Cài đặt Model")
        
        # Thêm tooltip giải thích về các model
        model = st.selectbox(
            "Model",
            options=AVAILABLE_MODELS,
            index=AVAILABLE_MODELS.index(DEFAULT_MODEL),
            help="""
            - claude-3.5-sonnet-2024-10-22: Model mới nhất và mạnh nhất, khuyên dùng cho hầu hết tác vụ
            - claude-3.5-sonnet-2024-06-20: Model ổn định, phù hợp cho các tác vụ yêu cầu độ tin cậy cao
            - claude-3.5-haiku: Model nhanh và nhẹ, phù hợp cho các tác vụ đơn giản cần phản hồi nhanh
            """
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=DEFAULT_TEMPERATURE,
            step=0.1,
            help="Điều chỉnh độ sáng tạo trong câu trả lời (0: ít sáng tạo, 1: nhiều sáng tạo)"
        )
        
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=4000,
            value=DEFAULT_MAX_TOKENS,
            step=100,
            help="Giới hạn độ dài tối đa của câu trả lời"
        )
        
        if st.button("🗑️ Xóa lịch sử"):
            st.session_state.chat_history = []
            st.experimental_rerun()

    # Main chat area
    chat_container = st.container()
    
    # Hiển thị lịch sử chat từ session state
    with chat_container:
        for idx, message in enumerate(st.session_state.chat_history):
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else None):
                st.write(message["content"])
                
                # Thêm nút copy cho response của assistant
                if message["role"] == "assistant":
                    create_copy_button(message["content"], f"copy_{idx}")
                
                # Thêm nút reset cho message của user
                if message["role"] == "user":
                    create_reset_button(idx, lambda i: chat_instance.reset_message(i))

    # Input area
    user_input = st.chat_input("Nhập câu hỏi của bạn...")
    
    if user_input:
        response = chat_instance.handle_message(
            message=user_input,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system=system_prompts[selected_bot]
        )
        
        # Hiển thị tin nhắn mới
        st.chat_message("user").write(user_input)
        with st.chat_message("assistant", avatar="🤖"):
            st.write(response)
            create_copy_button(response, f"copy_new")
