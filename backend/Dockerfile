FROM python:3.9-slim

WORKDIR /app

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 시작 스크립트
CMD ["sh", "-c", "echo 'Starting Backend Server on http://localhost:8000' && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]