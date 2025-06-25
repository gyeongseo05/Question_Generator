from jsonschema import validate, ValidationError

# 문제 자동 생성기 JSON 형식 정의 (Schema)
question_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["객관식","选择题"]},
        "difficulty": {"type": "string"},
        "question": {"type": "string"},
        "options": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 4,
            "maxItems": 4
        },
        "answer": {
            "type": "string",
            "pattern": "^[ABCD]$"
        },
        "explanation": {"type": "string"}
    },
    "required": ["type", "difficulty", "question", "options", "answer", "explanation"]
}

def validate_output(data):
    """LLM이 생성한 문제 JSON을 스키마로 검증합니다."""
    try:
        validate(instance=data, schema=question_schema)
        return True, None
    except ValidationError as ve:
        return False, str(ve)

# 테스트용 예시
if __name__ == "__main__":
    import json

    sample = {
        "type": "객관식",
        "difficulty": "쉬움",
        "question": "AI는 무엇을 모방하는 기술인가?",
        "options": ["A. 동물의 행동", "B. 자연 현상", "C. 인간의 사고", "D. 기계의 작동 원리"],
        "answer": "C",
        "explanation": "AI는 인간의 사고를 모방해 학습/추론 등을 수행함."
    }

    valid, err = validate_output(sample)
    if valid:
        print("✅ 유효한 형식입니다.")
    else:
        print("❌ 오류:", err)
