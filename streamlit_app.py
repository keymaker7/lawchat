import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(
    page_title="🌈 인권 지킴이 AI 챗봇",
    page_icon="🌈",
)

# 귀여운 스타일 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');
    
    /* 전체 배경 - 흰색 바탕 */
    [data-testid="stAppViewContainer"] > .main {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        background-attachment: fixed;
    }
    
    /* 메인 컨테이너 */
    .main > div {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        margin: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    /* 타이틀 스타일 */
    .main h1 {
        font-family: 'Jua', sans-serif;
        color: #2d3748;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(102, 126, 234, 0.2);
    }
    
    /* 캡션 스타일 */
    .main p {
        font-family: 'Jua', sans-serif;
        color: #4a5568;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    
    /* 채팅 메시지 스타일 */
    [data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    /* 사용자 메시지 */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20px;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* AI 메시지 */
    [data-testid="stChatMessage"][data-testid*="assistant"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: 20px;
        border: 1px solid rgba(245, 87, 108, 0.3);
    }
    
    /* 입력창 스타일 */
    [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 25px;
        border: 2px solid #667eea;
        padding: 10px 20px;
        font-family: 'Jua', sans-serif;
        font-size: 1.1rem;
    }
    
    /* 입력창 포커스 */
    [data-testid="stChatInput"]:focus {
        border-color: #764ba2;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    /* 스피너 스타일 */
    [data-testid="stSpinner"] {
        color: #667eea;
    }
    
    /* 귀여운 데코레이션 */
    .decoration {
        position: fixed;
        pointer-events: none;
        z-index: -1;
    }
    
    /* 법 관련 귀여운 아이콘들 */
    .law-icon {
        position: fixed;
        font-size: 30px;
        animation: float 3s ease-in-out infinite;
        opacity: 0.6;
        color: #667eea;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .law-icon-small {
        position: fixed;
        font-size: 20px;
        animation: bounce 2s ease-in-out infinite;
        opacity: 0.4;
        color: #764ba2;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* 하단 푸터 */
    .footer {
        position: fixed !important;
        right: 15px !important;
        bottom: 15px !important;
        background: rgba(255, 255, 255, 0.95) !important;
        color: #4a5568 !important;
        font-size: 0.85em !important;
        text-align: right !important;
        padding: 10px 15px !important;
        border-radius: 15px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        font-family: 'Jua', sans-serif !important;
        border: 1px solid rgba(102, 126, 234, 0.3) !important;
        z-index: 9999 !important;
        max-width: 300px !important;
        line-height: 1.3 !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 10px 20px;
        font-family: 'Jua', sans-serif;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 사이드바 숨기기 */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    /* 메뉴 버튼 숨기기 */
    [data-testid="stToolbar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# 귀여운 법 관련 배경 데코레이션
st.markdown("""
<div class="decoration">
    <!-- 법 관련 큰 아이콘들 -->
    <div class="law-icon" style="top: 10%; left: 10%;">⚖️</div>
    <div class="law-icon" style="top: 20%; left: 85%; animation-delay: 1s;">🏛️</div>
    <div class="law-icon" style="top: 70%; left: 15%; animation-delay: 2s;">📚</div>
    <div class="law-icon" style="top: 80%; left: 90%; animation-delay: 3s;">⚖️</div>
    <div class="law-icon" style="top: 50%; left: 5%; animation-delay: 4s;">🏛️</div>
    
    <!-- 법 관련 작은 아이콘들 -->
    <div class="law-icon-small" style="top: 30%; left: 25%; animation-delay: 0.5s;">📖</div>
    <div class="law-icon-small" style="top: 45%; left: 75%; animation-delay: 1.5s;">🎓</div>
    <div class="law-icon-small" style="top: 60%; left: 30%; animation-delay: 2.5s;">📜</div>
    <div class="law-icon-small" style="top: 25%; left: 60%; animation-delay: 3.5s;">🏛️</div>
    <div class="law-icon-small" style="top: 85%; left: 40%; animation-delay: 4.5s;">⚖️</div>
    <div class="law-icon-small" style="top: 15%; left: 40%; animation-delay: 5s;">📚</div>
    <div class="law-icon-small" style="top: 65%; left: 70%; animation-delay: 5.5s;">🎯</div>
    <div class="law-icon-small" style="top: 35%; left: 95%; animation-delay: 6s;">📖</div>
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

# 제목과 설명
st.title("🌈 인권 지킴이 AI 챗봇 🤖")
st.caption("🎯 궁금한 인권 침해 사례를 입력하면 AI가 친절하게 분석해 줄게요! 💝")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕! 🙋‍♀️ 나는 인권 지킴이 AI야! 🌟 궁금한 인권 침해 사례를 이야기해 주면, 내가 친절하게 분석해 줄게! 💪✨"}
    ]

# 채팅 메시지 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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

# 하단 푸터 (더 강력한 스타일링)
st.markdown("""
<div class="footer">
    디지털 기반 학생 맞춤교육, AI정보교육 중심학교<br>
    효행초등학교 - 김종윤
</div>
""", unsafe_allow_html=True)

# 추가적인 푸터 (만약 위의 것이 안 보이면)
st.markdown("""
<style>
    .custom-footer {
        position: fixed;
        right: 10px;
        bottom: 10px;
        background: white;
        color: #4a5568;
        font-size: 12px;
        text-align: right;
        padding: 8px 12px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        z-index: 999999;
        font-family: 'Jua', sans-serif;
    }
</style>
<div class="custom-footer">
    디지털 기반 학생 맞춤교육, AI정보교육 중심학교<br>효행초등학교 - 김종윤
</div>
""", unsafe_allow_html=True)
