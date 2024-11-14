import json
import anthropic
import streamlit as st
from typing import List, Dict
from config.settings import (
    CONFIG_FILE,
    MAX_HISTORY_MESSAGES,
    RECENT_MESSAGES_LIMIT,
    DEFAULT_MODEL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_SYSTEM_PROMPT
)
from utils.config import ConfigManager

class ClaudeChat:
    def __init__(self, config_file: str = CONFIG_FILE):
        self.config_file = config_file
        self.config_manager = ConfigManager(config_file)
        self.client = None
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        self._initialize_client()

    def get_api_key(self) -> str:
        try:
            config = self.config_manager.load_config()
            api_key = config.get('anthropic_api_key')
            if not api_key:
                raise ValueError(f"Không tìm thấy anthropic_api_key trong config")
            return api_key
        except Exception as e:
            raise ValueError(f"Lỗi khi lấy API key: {str(e)}")

    def _initialize_client(self) -> None:
        try:
            api_key = self.get_api_key()
            self.client = anthropic.Anthropic(api_key=api_key)
        except ValueError as e:
            st.error(f"Lỗi khi khởi tạo client: {str(e)}")
            raise

    def get_recent_messages(self, limit: int = RECENT_MESSAGES_LIMIT) -> List[Dict[str, str]]:
        """Lấy n tin nhắn gần nhất từ lịch sử chat"""
        return st.session_state.chat_history[-limit:] if st.session_state.chat_history else []

    def send_message(
        self,
        prompt: str,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        system: str = DEFAULT_SYSTEM_PROMPT
    ) -> str:
        if not prompt.strip():
            return ""

        try:
            # Lấy tin nhắn gần nhất từ lịch sử
            recent_messages = self.get_recent_messages()
            
            # Tạo danh sách messages cho API call, bao gồm lịch sử
            messages = [{"role": msg["role"], "content": msg["content"]} for msg in recent_messages]
            # Thêm tin nhắn hiện tại
            messages.append({"role": "user", "content": prompt})

            # Gọi Claude API với toàn bộ context
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system,
                messages=messages
            )

            # Trích xuất text từ response
            message_content = response.content[0].text if response.content else "Không có phản hồi"
            
            # Cập nhật lịch sử chat trong session state
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({"role": "assistant", "content": message_content})
            
            # Giới hạn lịch sử chat để không quá dài
            if len(st.session_state.chat_history) > MAX_HISTORY_MESSAGES:
                st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY_MESSAGES:]
            
            return message_content

        except Exception as e:
            error_message = f"Lỗi khi gửi tin nhắn: {str(e)}"
            st.error(error_message)
            return f"🚫 {error_message}"
