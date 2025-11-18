import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# 세션 상태 초기화
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'checklist_done' not in st.session_state:
    st.session_state['checklist_done'] = []

# ------------------------------
# 홈 화면
# ------------------------------
st.title("🐶 Pet AI Helper")
st.write("홈 화면에서 기능을 선택하세요.")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("1️⃣ 입양 적합성 & 품종 추천"):
        st.session_state['page'] = 'recommend'
with col2:
    if st.button("2️⃣ 예방접종 & 건강 루틴"):
        st.session_state['page'] = 'health'
with col3:
    if st.button("3️⃣ 증상 Q&A"):
        st.session_state['page'] = 'symptom'

col4, col5 = st.columns(2)
with col4:
    if st.button("4️⃣ 동물병원/보험 비교"):
        st.session_state['page'] = 'hospital_insurance'
with col5:
    if st.button("5️⃣ 커뮤니티"):
        st.session_state['page'] = 'community'

# ------------------------------
# 1️⃣ 입양 적합성 & 품종 추천
# ------------------------------
if st.session_state['page'] == 'recommend':
    st.header("입양 적합성 & 품종 추천")

    # 사용자 입력
    working_hours = st.number_input("근무시간 (시간/일)", min_value=0, max_value=24, value=8)
    home_type = st.selectbox("주거형태", ["아파트", "단독주택", "기타"])
    activity = st.slider("활동성", 1, 5, 3)
    budget = st.number_input("월 예산 (원)", min_value=0, step=10000)  # 직접 입력 가능
    allergy = st.selectbox("알레르기 여부", ["없음", "있음"])
    noise = st.slider("소음 허용도", 1, 5, 3)

    if st.button("추천받기"):
        # 간단 추천 로직 (데이터 없으므로 예시)
        recommended_breeds = ["1번: 시바견", "2번: 말티즈", "3번: 푸들"]
        difficulty = "초보 가능"
        checklist = ["사료", "배변패드", "목줄", "장난감"]
        st.session_state['checklist_done'] = [False]*len(checklist)

        st.subheader("추천 품종")
        for b in recommended_breeds:
            st.write(b)
        st.write("난이도:", difficulty)
        st.write("예상 월 비용:", budget, "원")

        st.subheader("필수 준비물 체크리스트")
        for i, item in enumerate(checklist):
            st.session_state['checklist_done'][i] = st.checkbox(item, value=st.session_state['checklist_done'][i])

# ------------------------------
# 2️⃣ 예방접종 & 건강 루틴
# ------------------------------
elif st.session_state['page'] == 'health':
    st.header("예방접종 & 건강 루틴")
    breeds = ["시바견","말티즈","푸들","진도견","골든리트리버","포메라니안","비글","치와와","닥스훈트","보더콜리",
              "요크셔테리어","푸들","래브라도","사모예드","슈나우저","웰시코기","보스턴테리어","셰틀랜드쉽독","말라뮤트","기타"]
    breed = st.selectbox("품종 선택", breeds)
    age = st.number_input("나이(개월)", min_value=1, max_value=240, value=12)

    if breed:
        # 예방접종 예시
        st.subheader(f"{breed} 권장 예방접종 스케줄")
        st.write("예시: 종합백신, 광견병, 코로나 등 (자동 계산)")

    # 건강 루틴 기록
    st.subheader("건강 루틴 기록")
    weight = st.number_input("체중 (kg)", min_value=0.0, step=0.1)
    poop_pattern = st.selectbox("배변 패턴", ["정상", "빈번", "불규칙"])
    date = st.date_input("기록 날짜", datetime.today())

    if st.button("기록 저장"):
        st.success("기록 저장 완료")
        # 그래프 예시
        st.subheader("체중 변화 그래프")
        dates = [datetime.today().date()]
        weights = [weight]
        plt.plot(dates, weights, marker='o')
        plt.xlabel("날짜")
        plt.ylabel("체중(kg)")
        st.pyplot(plt)

# ------------------------------
# 3️⃣ 증상 Q&A
# ------------------------------
elif st.session_state['page'] == 'symptom':
    st.header("증상 Q&A")
    symptom = st.text_input("증상 입력")
    if st.button("검색"):
        st.write(f"입력하신 증상 '{symptom}' 기반 자가 처치 금지 / 위험 신호 안내 예시")

# ------------------------------
# 4️⃣ 동물병원/보험 비교
# ------------------------------
elif st.session_state['page'] == 'hospital_insurance':
    st.header("동물병원 / 보험 비교")
    location = st.text_input("지역 입력", "서울")
    st.write(f"{location} 근처 동물병원 지도 표시 (더미 데이터)")
    st.write("보험 비교 예시: 보장 범위, 자기부담률")

# ------------------------------
# 5️⃣ 커뮤니티
# ------------------------------
elif st.session_state['page'] == 'community':
    st.header("커뮤니티")
    post = st.text_input("게시글 입력")
    if st.button("게시글 등록"):
        st.success(f"게시글 등록 완료: {post}")
        st.write(f"💬 {post}")
    st.subheader("댓글")
    comment = st.text_input("댓글 입력")
    if st.button("댓글 등록"):
        st.success(f"댓글 등록 완료: {comment}")
        st.write(f"↳ {comment}")
