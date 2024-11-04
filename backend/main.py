from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os
from pydantic import BaseModel
from typing import List, Optional, Dict, Union
import datetime
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    text: str

class WeatherResponse(BaseModel):
    question: str
    answer: Union[Dict, str]  # answer can be either a dict or string
    timestamp: str

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/forecast"

CITY_MAPPING: Dict[str, str] = {
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
    "고양시": "Goyang",
    "안양시": "Anyang",
    "수원시": "Suwon",
    "하와이": "Hawaii"
}

def parse_location_from_text(text: str) -> str:
    text = text.replace(" ", "")  # 공백 제거
    for city in CITY_MAPPING.keys():
        if city in text:
            return city
    return "서울"  # 기본값

def parse_time_from_text(text: str) -> str:
    if "모레" in text:
        return "after_tomorrow"
    elif "내일" in text:
        return "tomorrow"
    return "current"

def extract_location_and_time(text: str):
    return parse_location_from_text(text), parse_time_from_text(text)

async def get_forecast_data(city: str, time_type: str):
    async with httpx.AsyncClient() as client:
        try:
            city_eng = CITY_MAPPING.get(city, city)
            
            params = {
                "q": f"{city_eng},KR",
                "appid": OPENWEATHER_API_KEY,
                "lang": "kr",
                "units": "metric"
            }
            
            if city == "하와이":
                params["q"] = "Hawaii,US"
            
            if time_type == "current":
                response = await client.get(WEATHER_API_URL, params=params)
            else:
                response = await client.get(FORECAST_API_URL, params=params)
            
            if response.status_code != 200:
                data = response.json()
                raise HTTPException(status_code=response.status_code, 
                                  detail=data.get('message', '날씨 정보를 가져오는데 실패했습니다.'))
            
            data = response.json()
            
            if time_type == "current":
                return data
            else:
                tz = pytz.timezone('Asia/Seoul')
                now = datetime.datetime.now(tz)
                days_to_add = 1 if time_type == "tomorrow" else 2
                target_date = now.date() + datetime.timedelta(days=days_to_add)
                
                # 해당 날짜의 정오 데이터 찾기
                for item in data['list']:
                    forecast_time = datetime.datetime.fromtimestamp(item['dt'], tz=tz)
                    if forecast_time.date() == target_date and forecast_time.hour >= 12:
                        return item
                
                # 못 찾은 경우 첫 번째 예보 데이터 반환
                return data['list'][0]
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"날씨 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")

def generate_weather_response(weather_data: dict, time_type: str, city: str) -> dict:
    try:
        temp = round(float(weather_data["main"]["temp"]), 1)
        humidity = weather_data["main"]["humidity"]
        description = weather_data["weather"][0]["description"]
        icon = weather_data["weather"][0]["icon"]
        
        time_text = "현재" if time_type == "current" else "내일" if time_type == "tomorrow" else "모레"
        
        return {
            "text": f"{city}의 {time_text} 날씨입니다. 기온은 {temp}°C이고, 습도는 {humidity}%입니다. 날씨는 {description} 상태입니다.",
            "icon": icon,
            "temp": temp,
            "humidity": humidity,
            "description": description
        }
    except Exception as e:
        return {
            "text": "날씨 정보 처리 중 오류가 발생했습니다.",
            "icon": "unknown",
            "temp": 0,
            "humidity": 0,
            "description": "알 수 없음"
        }

@app.post("/api/ask")
async def ask_weather(question: Question):
    try:
        location, time_type = extract_location_and_time(question.text)
        weather_data = await get_forecast_data(location, time_type)
        answer = generate_weather_response(weather_data, time_type, location)
        
        return WeatherResponse(
            question=question.text,
            answer=answer,
            timestamp=datetime.datetime.now(pytz.timezone('Asia/Seoul')).isoformat()
        )
    except HTTPException as e:
        return WeatherResponse(
            question=question.text,
            answer={"text": f"죄송합니다. {str(e.detail)}", "icon": "unknown"},
            timestamp=datetime.datetime.now(pytz.timezone('Asia/Seoul')).isoformat()
        )
    except Exception as e:
        return WeatherResponse(
            question=question.text,
            answer={"text": "죄송합니다. 날씨 정보를 처리하는 중에 오류가 발생했습니다.", "icon": "unknown"},
            timestamp=datetime.datetime.now(pytz.timezone('Asia/Seoul')).isoformat()
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)