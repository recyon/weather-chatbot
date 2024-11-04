# 날씨 채팅봇 프로젝트

React와 FastAPI를 활용한 웹 접근성을 준수한 날씨 정보 채팅봇 애플리케이션입니다. 사용자는 자연어로 날씨에 대해 질문할 수 있으며, OpenWeatherMap API를 통해 실시간 날씨 정보를 제공받을 수 있습니다.

## 데모 화면
![날씨 채팅봇 데모](demo.gif)
- 채팅형 인터페이스로 자연스러운 날씨 질문/응답
- 실시간 날씨 아이콘 표시
- 웹 접근성이 고려된 UI/UX 적용

## 주요 기능

- 자연어 날씨 질문 입력
- 실시간 날씨 정보 제공
- 날씨 아이콘으로 직관적인 정보 전달
- 대화 히스토리 관리 및 자동 스크롤
- 다양한 도시 지원
- 현재/내일/모레 날씨 정보 제공
- 웹 접근성 준수 (WCAG 2.1 지침 준수)

## 기술 스택

### Frontend
- React 18
- TypeScript 4.9
- Recoil (상태 관리)
- Tailwind CSS
- ARIA (접근성)

### Backend
- FastAPI
- Python 3.9
- OpenWeatherMap API
- asyncio & httpx

### DevOps
- Docker
- Docker Compose

## 프로젝트 구조

```
weather-chatbot/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── WeatherChat.tsx        # 접근성이 향상된 메인 채팅 컴포넌트
│   │   ├── recoil/
│   │   │   └── atoms.ts               # 전역 상태 관리
│   │   ├── types/
│   │   │   └── index.ts               # TypeScript 타입 정의
│   │   ├── App.tsx                    # 앱 메인 컴포넌트
│   │   └── index.tsx                  # 앱 엔트리 포인트
│   ├── Dockerfile
│   └── package.json
├── backend/
│   ├── main.py                        # FastAPI 백엔드 서버
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## 실행 방법

1. 필요 조건
- Docker 및 Docker Compose 설치
- OpenWeatherMap API 키 발급

2. 환경 변수 설정
```bash
echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
```

3. Docker Compose로 실행
```bash
# 일반 실행
docker compose up

# 백그라운드 실행
docker compose up -d

# 변경사항이 있을 때 재빌드
docker compose up --build
```

4. 접속 URL
```
프론트엔드: http://localhost:3000
백엔드: http://localhost:8000

# API 엔드포인트
날씨 질문: http://localhost:8000/api/ask [POST]

# Swagger API 문서
http://localhost:8000/docs
```

## 사용 예시

```
- "서울 날씨 어때?"          # 현재 날씨
- "부산 내일 날씨 알려줘"    # 내일 날씨
- "제주도 모레 날씨"         # 모레 날씨
- "안양시 날씨"             # 지역 날씨
```

## 웹 접근성 준수 사항

### 1. 키보드 접근성
- Tab 키로 모든 기능 사용 가능
- 포커스 표시자 명확히 제공
- 키보드 트랩 방지
- 단축키 제공 및 안내

### 2. 스크린 리더 지원
- ARIA 레이블링
- 실시간 콘텐츠 업데이트 알림
- 이미지 대체 텍스트
- 상태 변경 알림

### 3. 시각적 디자인
- WCAG 2.1 기준 색상 대비
- 반응형 디자인
- 오류 상태의 시각적 표시

## 개발 및 유지보수

### 도커 관련 명령어
```bash
# 로그 보기
docker compose logs -f

# 특정 서비스 로그 보기
docker compose logs frontend -f
docker compose logs backend -f

# 서비스 재시작
docker compose restart frontend
docker compose restart backend

# 전체 중지
docker compose down
```

### 코드 수정 시
```bash
# 코드 수정 후 재시작
docker compose down
docker compose up --build
```

## API 명세

### POST /api/ask
날씨 정보 요청 API

Request Body:
```json
{
  "text": "서울 내일 날씨 어때?"
}
```

Response:
```json
{
  "question": "서울 내일 날씨 어때?",
  "answer": {
    "text": "서울의 내일 날씨입니다. 기온은 12.8°C이고, 습도는 42%입니다. 날씨는 흐림 상태입니다.",
    "icon": "04d",
    "temp": 12.8,
    "humidity": 42,
    "description": "흐림"
  },
  "timestamp": "2024-11-04T09:05:14+09:00"
}
```

## 지원하는 도시 목록
```python
CITY_MAPPING = {
    "서울": "Seoul",
    "부산": "Busan",
    "대구": "Daegu",
    "인천": "Incheon",
    "광주": "Gwangju",
    "대전": "Daejeon",
    "울산": "Ulsan",
    "제주": "Jeju",
    "안양": "Anyang",
    "고양": "Goyang",
    "성남": "Seongnam",
    "수원": "Suwon",
    "용인": "Yongin",
    "부천": "Bucheon",
    "안산": "Ansan",
    # ... 기타 도시들
}
```

## 개선 계획
1. 더 많은 도시 지원 추가
2. 음성 입력 기능
3. 키보드 단축키 확장
4. 다크 모드 지원
5. 날씨 알림 기능
6. 상세 날씨 정보 제공

## 문제 해결

### 자주 발생하는 문제
1. Docker 실행 오류
```bash
# Docker 캐시 삭제
docker system prune -a
```

2. 패키지 설치 오류
```bash
# frontend의 경우
rm -rf frontend/node_modules
rm frontend/package-lock.json
docker compose up --build

# backend의 경우
docker compose exec backend pip install -r requirements.txt
```

3. API 연결 오류
- .env 파일의 API 키 확인
- 네트워크 설정 확인
- 백엔드 서비스 로그 확인

## 라이센스
MIT License

## 기여 방법
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 작성자
- GitHub: [Your GitHub]
- Email: [Your Email]

---
이 프로젝트는 웹 접근성과 사용자 경험을 중시하며, 지속적인 개선을 통해 더 나은 서비스를 제공하고자 합니다.