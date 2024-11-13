import streamlit as st
from src.controllers.chat_controller import ChatController
from src.views.ui import create_chat_ui
from src.utils.config import ConfigManager, SystemPromptsManager

def main():
    try:
        # Khởi tạo các managers
        config_manager = ConfigManager()
        system_prompts_manager = SystemPromptsManager()
        
        # Khởi tạo controller
        chat_controller = ChatController()
        
        # Tạo và chạy giao diện
        create_chat_ui(chat_controller)
        
    except Exception as e:
        st.error(f"Lỗi khởi động ứng dụng: {str(e)}")

if __name__ == "__main__":
    main()
