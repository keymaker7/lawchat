import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(
    page_title="🌈 인권 지킴이 AI 챗봇",
    page_icon="🌈",
)

# 깔끔한 UI 스타일 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    
    /* 전체 배경 - 깔끔한 흰색 */
    [data-testid="stAppViewContainer"] > .main {
        background: #ffffff;
        padding: 0;
    }
    
    /* 헤더 영역 */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px 20px;
        border-radius: 0 0 30px 30px;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
    }
    
    /* 타이틀 스타일 */
    .main-title {
        font-family: 'Jua', sans-serif;
        color: white;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* 캡션 스타일 */
    .main-caption {
        font-family: 'Jua', sans-serif;
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin: 10px 0 0 0;
    }
    
    /* 채팅 컨테이너 */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 0 20px;
    }
    
    /* 채팅 메시지 스타일 */
    [data-testid="stChatMessage"] {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 2px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid #f0f0f0;
        font-family: 'Jua', sans-serif;
    }
    
    /* 사용자 메시지 */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 60px;
        margin-right: 0;
    }
    
    /* AI 메시지 */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: 60px;
        margin-left: 0;
    }
    
    /* 입력창 스타일 */
    [data-testid="stChatInput"] {
        background: white;
        border-radius: 30px;
        border: 2px solid #667eea;
        padding: 15px 25px;
        font-family: 'Jua', sans-serif;
        font-size: 1.1rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.1);
    }
    
    /* 입력창 포커스 */
    [data-testid="stChatInput"]:focus {
        border-color: #764ba2;
        box-shadow: 0 4px 25px rgba(102, 126, 234, 0.2);
        outline: none;
    }
    
    /* 스피너 스타일 */
    [data-testid="stSpinner"] {
        color: #667eea;
    }
    
    /* 법 관련 배경 아이콘들 */
    .law-decoration {
        position: fixed;
        pointer-events: none;
        z-index: 0;
        font-size: 25px;
        opacity: 0.1;
        color: #667eea;
        animation: float 4s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }
    
    /* 하단 좌측 푸터 */
    .footer-left {
        position: fixed;
        left: 20px;
        bottom: 20px;
        background: white;
        color: #4a5568;
        font-size: 0.9em;
        padding: 12px 18px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        font-family: 'Jua', sans-serif;
        border: 2px solid #667eea;
        z-index: 1000;
        line-height: 1.4;
        max-width: 280px;
    }
    
    /* 사이드바 숨기기 */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* 메뉴 버튼 숨기기 */
    [data-testid="stToolbar"] {
        display: none;
    }
    
    /* Streamlit 기본 여백 제거 */
    .main .block-container {
        padding-top: 0;
        padding-bottom: 100px;
    }
</style>
""", unsafe_allow_html=True)

# 배경 장식 아이콘들 (적당히 배치)
st.markdown("""
<div style="position: relative;">
    <div class="law-decoration" style="top: 150px; left: 50px; animation-delay: 0s;">⚖️</div>
    <div class="law-decoration" style="top: 250px; right: 80px; animation-delay: 1s;">🏛️</div>
    <div class="law-decoration" style="top: 400px; left: 100px; animation-delay: 2s;">📚</div>
    <div class="law-decoration" style="top: 500px; right: 150px; animation-delay: 3s;">📖</div>
    <div class="law-decoration" style="top: 300px; left: 200px; animation-delay: 4s;">🎓</div>
    <div class="law-decoration" style="top: 600px; right: 200px; animation-delay: 5s;">📜</div>
</div>
""", unsafe_allow_html=True)

# API 키 설정
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("🚨 API 키를 설정하는 중에 오류가 발생했습니다. Streamlit Secrets에 GEMINI_API_KEY가 올바르게 설정되었는지 확인해주세요.")
    st.stop()

# 마스터 프롬프트
MASTER_PROMPT = """
너는 대한민국의 초등학교 5학년 학생들을 위한 '인권 지킴이 AI 챗봇'이야. 학생의 눈높이에서 인권 침해 사례를 분석하고 설명하는 임무를 맡고 있어. 다음 규칙을 반드시 지켜줘.

1. 친절한 대화: 항상 상냥하고 격려하는 말투로 학생과 대화해. 어려운 법률 용어는 절대 사용하지 마.
2. 단계별 분석: 학생이 인권 침해 사례를 입력하면, 4단계에 따라 순서대로 답변해야 해. (1단계: 어떤 인권 침해?, 2단계: 관련 법 찾아보기, 3단계: 법 쉽게 설명하기, 4단계: AI의 생각 나누기)
3. 주제 유지: 인권과 관련 없는 질문에는 "나는 인권 박사님이라서, 인권에 대한 이야기만 할 수 있어."라고 대답해 줘.
4. 개인정보 보호: 학생에게 개인적인 정보는 절대 묻지 마.
"""

# 모델 초기화
model = genai.GenerativeModel('gemini-1.5-flash')

# 헤더 영역
st.markdown("""
<div class="header-container">
    <h1 class="main-title">🌈 인권 지킴이 AI 챗봇 🤖</h1>
    <p class="main-caption">🎯 궁금한 인권 침해 사례를 입력하면 AI가 친절하게 분석해 줄게요! 💝</p>
</div>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕! 🙋‍♀️ 나는 인권 지킴이 AI야! 🌟 궁금한 인권 침해 사례를 이야기해 주면, 내가 친절하게 분석해 줄게! 💪✨"}
    ]

# 채팅 메시지 표시
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# 사용자 입력 처리
if prompt := st.chat_input("🎈 여기에 사례를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🤔 AI가 열심히 생각 중이에요..."):
            full_prompt = f"{MASTER_PROMPT}\n\n학생의 질문: {prompt}"
            response = model.generate_content(full_prompt)
            response_text = response.text
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

# 하단 좌측 푸터
st.markdown("""
<div class="footer-left">
    💻 디지털 기반 학생 맞춤교육<br>
    🤖 AI정보교육 중심학교<br>
    🏫 효행초등학교 - 김종윤
</div>
""", unsafe_allow_html=True)
