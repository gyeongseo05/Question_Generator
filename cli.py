# cli.py
from question_generator import generate_question

def main():
    print("📘 문제 자동 생성기")
    print("사용자가 입력한 내용을 기반으로 객관식 문제를 생성합니다.")
    print("=" * 40)

    context = input("📄 본문 입력: ")
    difficulty = input("🧠 난이도 선택 (쉬움/보통/어려움): ")

    print("\n⏳ 문제 생성 중...\n")
    result = generate_question(context, difficulty)

    print("🎯 생성된 문제:")
    print(result)

if __name__ == "__main__":
    main()
