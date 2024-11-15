import json
from typing import Dict, Any
from pathlib import Path

try:
    import streamlit as st
except ImportError:
    st = None

class ConfigManager:
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file

    def load_config(self) -> Dict[str, Any]:
        """Đọc config từ file hoặc streamlit secrets"""
        # Thử đọc từ file config.json trước
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                # Kiểm tra cả key chữ hoa và chữ thường
                api_key = config.get('ANTHROPIC_API_KEY') or config.get('anthropic_api_key')
                if api_key:
                    return {
                        "anthropic_api_key": api_key,
                        "model": config.get("model", "claude-2"),
                        "temperature": config.get("temperature", 0.7),
                        "max_tokens": config.get("max_tokens", 1000)
                    }
                
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Thử đọc từ Streamlit secrets
        if st is not None and hasattr(st, 'secrets') and 'anthropic' in st.secrets:
            return {
                "anthropic_api_key": st.secrets["anthropic"]["api_key"],
                "model": "claude-2",
                "temperature": 0.7,
                "max_tokens": 1000
            }

        raise ValueError(f"Không tìm thấy API key trong file {self.config_file} hoặc Streamlit secrets")

    def save_config(self, config: Dict[str, Any]) -> None:
        """Lưu config vào file"""
        # Chỉ lưu vào file khi chạy local
        if st is None or not hasattr(st, 'secrets'):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

class SystemPromptsManager:
    def __init__(self, prompts_file: str = 'src/data/system_prompts.json'):
        self.prompts_file = prompts_file
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Đảm bảo file system prompts tồn tại"""
        prompts_path = Path(self.prompts_file)
        if not prompts_path.exists():
            default_prompts = {
                "Default": "You are Mr. 'Lễ đẹp trai' a helpful AI assistant. Respond in Vietnamese."
            }
            prompts_path.parent.mkdir(parents=True, exist_ok=True)
            with open(prompts_path, 'w', encoding='utf-8') as f:
                json.dump(default_prompts, f, ensure_ascii=False, indent=2)

    def load_prompts(self) -> Dict[str, str]:
        """Đọc system prompts từ file"""
        try:
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "Default": "You are Mr. 'Lễ đẹp trai' a helpful AI assistant. Respond in Vietnamese."
            }

    def save_prompts(self, prompts: Dict[str, str]) -> None:
        """Lưu system prompts vào file"""
        with open(self.prompts_file, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)

    def add_prompt(self, name: str, prompt: str) -> None:
        """Thêm system prompt mới"""
        prompts = self.load_prompts()
        prompts[name] = prompt
        self.save_prompts(prompts)

    def update_prompt(self, name: str, prompt: str) -> None:
        """Cập nhật system prompt"""
        prompts = self.load_prompts()
        if name in prompts:
            prompts[name] = prompt
            self.save_prompts(prompts)
        else:
            raise ValueError(f"Không tìm thấy system prompt: {name}")

    def delete_prompt(self, name: str) -> None:
        """Xóa system prompt"""
        prompts = self.load_prompts()
        if name in prompts:
            del prompts[name]
            self.save_prompts(prompts)
        else:
            raise ValueError(f"Không tìm thấy system prompt: {name}")
