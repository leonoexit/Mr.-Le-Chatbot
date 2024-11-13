"""
Các cài đặt mặc định cho ứng dụng
"""

# Claude API settings
DEFAULT_MODEL = "claude-3-5-sonnet-20241022"  # Model mặc định
AVAILABLE_MODELS = [  # Danh sách các model có sẵn
    "claude-3-5-sonnet-20241022",  # Model mới nhất, khuyên dùng
    "claude-3-5-haiku-20241022"      # Model nhanh và nhẹ
]
DEFAULT_MAX_TOKENS = 1000
DEFAULT_TEMPERATURE = 0.7

# UI settings
PAGE_TITLE = "Mr Lễ AI"
PAGE_ICON = "🤖"
PAGE_LAYOUT = "wide"

# File paths
CONFIG_FILE = "config.json"
SYSTEM_PROMPTS_FILE = "src/data/system_prompts.json"

# Chat settings
MAX_HISTORY_MESSAGES = 20  # Số lượng tin nhắn tối đa trong lịch sử
RECENT_MESSAGES_LIMIT = 10  # Số lượng tin nhắn gần nhất để gửi cho API

# Default system prompt
DEFAULT_SYSTEM_PROMPT = "You are Mr. 'Lễ AI' a helpful AI assistant. Respond in Vietnamese."
