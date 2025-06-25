import streamlit as st
from question_generator import generate_question

st.set_page_config(page_title="문제 자동 생성기", page_icon="📘", layout="centered")

# --- 언어 선택
language = st.selectbox("🌐 언어 선택 / Language", ["한국어", "中文"])

# --- 텍스트 다국어 설정
texts = {
    "한국어": {
        "title": "📘 문제 자동 생성기 (LLM 기반)",
        "desc": "본문 내용을 입력하고 난이도를 선택하면 GPT가 자동으로 객관식 문제를 만들어줍니다.",
        "input": "📄 본문 입력",
        "difficulty": "🧠 난이도 선택",
        "temperature": "🌡️ 창의성 조절 (temperature)",
        "generate": "✅ 문제 생성하기",
        "result": "🎯 생성된 문제:",
        "choose": "정답을 선택하세요:",
        "check": "🔍 정답 확인하기",
        "correct": "🎉 정답입니다!",
        "wrong": "❌ 오답입니다. 정답은",
        "explanation": "📘 **해설:**",
        "error": "❌ 문제 형식이 올바르지 않습니다. 다시 시도해주세요.",
        "placeholder": "예: 인공지능은 인간의 사고를 모방하여 학습, 추론, 판단을 수행하는 기술이다."
    },
    "中文": {
        "title": "📘 问题自动生成器（基于LLM）",
        "desc": "请输入正文内容并选择难度，系统将自动生成选择题。",
        "input": "📄 正文输入",
        "difficulty": "🧠 难度选择",
        "temperature": "🌡️ 创意控制（temperature）",
        "generate": "✅ 生成问题",
        "result": "🎯 生成的问题：",
        "choose": "请选择正确答案：",
        "check": "🔍 检查答案",
        "correct": "🎉 恭喜你，答对了！",
        "wrong": "❌ 很遗憾，正确答案是",
        "explanation": "📘 **解析：**",
        "error": "❌ 问题格式错误，请重试。",
        "placeholder": "例如：人工智能是一种模拟人类思维、进行学习与推理的技术。"
    }
}

t = texts[language]

st.title(t["title"])
st.markdown(t["desc"])

# --- 사용자 입력
context = st.text_area(t["input"], placeholder=t["placeholder"])
difficulty = st.selectbox(t["difficulty"], ["쉬움", "보통", "어려움"] if language == "한국어" else ["简单", "中等", "困难"])
temperature = st.slider(t["temperature"], 0.0, 1.5, 0.7, step=0.05)

# --- 상태 저장
if "generated" not in st.session_state:
    st.session_state.generated = None
if "selected" not in st.session_state:
    st.session_state.selected = None

# --- 문제 생성
if st.button(t["generate"]) and context.strip():
    st.session_state.generated = generate_question(context, difficulty=difficulty, temperature=temperature, language=language)
    st.session_state.selected = None

# --- 문제 출력
question_data = st.session_state.generated
if question_data:
    st.divider()
    st.subheader(t["result"])

    st.markdown(f"**Q. {question_data.get('question')}**")
    selected_option = st.radio(t["choose"], question_data["options"], index=None, key="selected_option")

    if st.button(t["check"]) and selected_option:
        correct = question_data.get("answer")
        if selected_option.startswith(correct + "."):
            st.success(t["correct"])
        else:
            st.error(f"{t['wrong']} **{correct}**")
        st.markdown(f"{t['explanation']} {question_data.get('explanation')}")

elif context and not question_data:
    st.error(t["error"])