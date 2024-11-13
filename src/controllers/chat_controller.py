from typing import Dict, Any
import streamlit as st
from src.models.chat_model import ClaudeChat

class ChatController:
    def __init__(self):
        self.chat_model = ClaudeChat()
        
    def handle_message(self, 
                      message: str, 
                      model: str,
                      temperature: float,
                      max_tokens: int,
                      system: str) -> str:
        """Xử lý tin nhắn từ người dùng"""
        return self.chat_model.send_message(
            prompt=message,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system=system
        )
    
    def reset_message(self, index: int) -> None:
        """Xóa tin nhắn tại vị trí index và tin nhắn trả lời tương ứng"""
        if index < len(st.session_state.chat_history):
            # Xóa tin nhắn của user
            st.session_state.chat_history.pop(index)
            # Xóa tin nhắn trả lời của assistant (nếu có)
            if index < len(st.session_state.chat_history):
                st.session_state.chat_history.pop(index)
    
    def clear_history(self) -> None:
        """Xóa toàn bộ lịch sử chat"""
        st.session_state.chat_history = []
