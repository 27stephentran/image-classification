# Sử dụng Python image nhẹ hơn
FROM python:3.11-slim

# Đặt biến môi trường
ENV PYTHONUNBUFFERED=1

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt trước để tối ưu layer cache
COPY requirements.txt .

# Cài đặt dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ code vào container
COPY . .

# Mở đúng cổng mà Render yêu cầu (thường là 10000 hoặc 8080)
EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
