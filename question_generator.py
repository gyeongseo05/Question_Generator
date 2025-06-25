import os
import requests
import json
import re
import time
from dotenv import load_dotenv
from validator import validate_output  # JSON 스키마 검증 함수 임포트

load_dotenv()
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/v1/chat/completions"

def extract_json(text):
    try:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            raise ValueError("JSON 형식을 찾을 수 없습니다.")
    except Exception as e:
        print(f"[JSON 파싱 오류] {e}")
        return None

def call_api_with_retry(payload, headers, retries=3, backoff=2):
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if hasattr(response, 'status_code') and response.status_code in [429, 500, 502, 503, 504]:
                print(f"⏳ 재시도 중... ({attempt + 1}/{retries})")
                time.sleep(backoff * (attempt + 1))
            else:
                raise e
    raise RuntimeError("❌ API 호출 실패 - 최대 재시도 횟수 초과")

def generate_question(context: str, difficulty: str = "보통", temperature: float = 0.7, language: str = "한국어"):
    if language == "中文":
        prompt = f"""
你是一个教育测验命题专家。请根据以下内容生成一个选择题（共4个选项：A、B、C、D），并提供正确答案和解释。
⚠️ 必须以 JSON 格式输出，并且不要添加多余的文字说明。

难度：{difficulty}
内容如下：
{context}

JSON 输出格式如下（请严格遵守）：
{{
  "type": "选择题",
  "difficulty": "{difficulty}",
  "question": "...",
  "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "answer": "C",
  "explanation": "..."
}}
"""
    else:
        prompt = f"""
너는 교육용 문제 출제 전문가야. 아래 내용을 바탕으로 객관식 문제를 1개 생성해 줘.
⚠️ 반드시 아래 JSON 형식 그대로만 출력하고, 텍스트 설명은 포함하지 마!

조건:
- 난이도는 "{difficulty}" 수준
- 보기 4개 (A, B, C, D)
- 정답과 해설 포함

본문:
{context}

응답 예시 (JSON 형식):
{{
  "type": "객관식",
  "difficulty": "{difficulty}",
  "question": "문제 내용",
  "options": [
    "A. ...",
    "B. ...",
    "C. ...",
    "D. ..."
  ],
  "answer": "C",
  "explanation": "정답에 대한 해설"
}}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }

    try:
        response_json = call_api_with_retry(payload, headers)
        content = response_json["choices"][0]["message"]["content"].strip()
        print("[🔍 원본 응답 보기]\n", content)

        result = extract_json(content)

        # 🔍 JSON 유효성 검증
        valid, error = validate_output(result)
        if not valid:
            print(f"[⚠️ JSON 검증 실패] {error}")
            return None

        return result

    except Exception as e:
        print(f"[오류 발생] {e}")
        return None


if __name__ == "__main__":
    context = "人工智能是一种模拟人类思维的技术，具备学习与推理能力。"
    result = generate_question(context, difficulty="简单", language="中文")
    if result:
        print("\n[✅ 最终输出结果]")
        print(json.dumps(result, indent=2, ensure_ascii=False))
