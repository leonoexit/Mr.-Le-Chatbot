# Claude Chat App

Ứng dụng chat với Claude AI sử dụng Streamlit với nhiều tính năng mới.

## Tính năng

- Chat với Claude AI với giao diện thân thiện
- Hỗ trợ các model Claude 3.5 mới nhất:
  - claude-3.5-sonnet-2024-10-22: Model mới nhất và mạnh nhất, khuyên dùng
  - claude-3.5-sonnet-2024-06-20: Model ổn định, độ tin cậy cao
  - claude-3.5-haiku: Model nhanh và nhẹ cho các tác vụ đơn giản
- Copy nhanh phản hồi của Claude bằng nút Copy
- Reset tin nhắn để chỉnh sửa nội dung
- Quản lý nhiều chatbot với system prompts khác nhau
- Lưu trữ lịch sử chat
- Tùy chỉnh các thông số như temperature, max tokens
- Giao diện người dùng thân thiện và dễ sử dụng

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd claude_api_streamlit
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Setup config:
- Copy file `config.example.json` thành `config.json`:
```bash
cp config.example.json config.json
```
- Mở file `config.json` và thêm API key của bạn vào:
```json
{
    "anthropic_api_key": "your-api-key-here",
    "model": "claude-2",
    "temperature": 0.7,
    "max_tokens": 1000
}
```

> ⚠️ **Lưu ý bảo mật**: 
> - File `config.json` chứa API key đã được thêm vào `.gitignore` để tránh bị push lên GitHub
> - KHÔNG BAO GIỜ commit file `config.json` lên repository
> - Nếu bạn vô tình commit API key, hãy thay đổi API key ngay lập tức
> - Mỗi người dùng cần tạo file `config.json` riêng theo mẫu trong `config.example.json`

## Chạy ứng dụng

Sử dụng script run.sh (recommended):
```bash
./run.sh
```

Hoặc chạy trực tiếp với Python:
```bash
PYTHONPATH=$PYTHONPATH:$(pwd) streamlit run src/main.py
```

## Cấu trúc project

```
src/
├── config/         # Cài đặt mặc định
│   ├── settings.py # Các thông số cấu hình
│   └── __init__.py
├── controllers/    # Logic điều khiển
│   ├── chat_controller.py
│   └── __init__.py
├── data/          # Dữ liệu
│   └── system_prompts.json  # Lưu trữ system prompts
├── models/        # Logic xử lý chat
│   ├── chat_model.py
│   └── __init__.py
├── utils/         # Tiện ích
│   ├── config.py  # Quản lý cấu hình
│   └── __init__.py
├── views/         # Giao diện người dùng
│   ├── ui.py      # Components UI
│   └── __init__.py
├── __init__.py
└── main.py        # File chính
```

## Quản lý Chatbots

1. Chọn chatbot có sẵn từ danh sách dropdown trong sidebar
2. Chỉnh sửa system prompt theo ý muốn và nhấn "Lưu thay đổi"
3. Tạo chatbot mới:
   - Điền tên chatbot mới
   - Nhập system prompt mới
   - Nhấn "Tạo mới"
4. Các chatbot được lưu tự động vào file system_prompts.json

## Tính năng Chat

1. Lựa chọn Model:
   - claude-3.5-sonnet-2024-10-22: Model mới nhất và mạnh nhất, khuyên dùng cho hầu hết tác vụ
   - claude-3.5-sonnet-2024-06-20: Model ổn định, phù hợp cho các tác vụ yêu cầu độ tin cậy cao
   - claude-3.5-haiku: Model nhanh và nhẹ, phù hợp cho các tác vụ đơn giản cần phản hồi nhanh

2. Copy Response:
   - Mỗi phản hồi của Claude có nút "Copy" để copy nhanh nội dung
   - Khi copy xong sẽ có thông báo "Đã copy!"

3. Reset Message:
   - Mỗi tin nhắn của người dùng có nút "Reset"
   - Nhấn Reset để xóa tin nhắn đó và phản hồi tương ứng
   - Có thể nhập lại nội dung mới

4. Tùy chỉnh:
   - Chọn model Claude phù hợp với nhu cầu
   - Điều chỉnh temperature để thay đổi độ sáng tạo
   - Điều chỉnh max tokens để kiểm soát độ dài câu trả lời

## Lưu ý

- Đảm bảo có API key hợp lệ trong file config.json
- Có thể tùy chỉnh các thông số mặc định trong src/config/settings.py
- Lịch sử chat được lưu trong phiên làm việc
- System prompts được lưu vào file json nên có thể dễ dàng sao lưu và khôi phục
- Chọn model phù hợp với nhu cầu sử dụng:
  + Dùng claude-3.5-sonnet-2024-10-22 cho hầu hết tác vụ
  + Dùng claude-3.5-sonnet-2024-06-20 khi cần độ tin cậy cao
  + Dùng claude-3.5-haiku khi cần phản hồi nhanh
