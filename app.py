import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Pet AI Helper", layout="wide")

# ----------------------------
# 사이드바 메뉴
menu = st.sidebar.selectbox("메뉴 선택", ["홈", "입양 적합성 & 품종 추천",
                                           "예방접종 & 건강 루틴", "증상 Q&A 안심가이드",
                                           "동물병원 & 보험 비교", "커뮤니티"])
# ----------------------------
# 0. 홈화면
if menu == "홈":
    st.title("🐾 Pet AI Helper 홈")
    st.write("원하는 기능을 선택하세요.")

# ----------------------------
# 1. 입양 적합성 & 품종 추천
elif menu == "입양 적합성 & 품종 추천":
    st.header("입양 적합성 & 품종 추천")
    
    with st.form("adoption_form"):
        st.subheader("사용자 정보 입력")
        work_hour = st.slider("근무시간 (시간/일)", 0, 12, 8)
        housing = st.selectbox("주거 형태", ["아파트", "단독주택", "오피스텔"])
        activity = st.slider("활동성", 1, 10, 5)
        budget = st.number_input("예산 (월간, 원 단위)", min_value=0, step=1000)
        allergy = st.radio("알레르기 여부", ["있음", "없음"])
        noise = st.slider("소음 허용도", 1, 10, 5)
        submitted = st.form_submit_button("추천받기")
    
    if submitted:
        # 간단 추천 로직 (예시)
        breeds = ["비글","푸들","말티즈","골든리트리버","시추",
                  "포메라니안","치와와","슈나우저","코기","요크셔테리어",
                  "달마시안","보스턴테리어","래브라도","닥스훈트","사모예드",
                  "웰시코기","페키니즈","허스키","진돗개","기타"]
        scores = np.random.rand(len(breeds))
        top_indices = np.argsort(scores)[::-1][:3]  # 상위 3개 추천
        top_breeds = [breeds[i] for i in top_indices]
        st.subheader("추천 품종")
        for idx, breed in enumerate(top_breeds, 1):
            st.write(f"{idx}. {breed}")
        
        # 체크리스트
        st.subheader("필수 준비물 체크리스트")
        items = ["사료", "물그릇", "배변패드", "장난감", "목줄"]
        checklist_states = []
        for item in items:
            checkbox = st.checkbox(item)
            checklist_states.append(checkbox)
        # 체크하면 화면 유지되도록 함

# ----------------------------
# 2. 예방접종 & 건강 루틴
elif menu == "예방접종 & 건강 루틴":
    st.header("예방접종 & 건강 루틴")
    
    breed_list = ["비글","푸들","말티즈","골든리트리버","시추",
                  "포메라니안","치와와","슈나우저","코기","요크셔테리어",
                  "달마시안","보스턴테리어","래브라도","닥스훈트","사모예드",
                  "웰시코기","페키니즈","허스키","진돗개","기타"]
    breed = st.selectbox("품종 선택", breed_list)
    age = st.number_input("나이 (개월)", min_value=0, max_value=240, value=12)
    
    if breed:
        st.subheader("권장 예방접종 스케줄")
        # 예시 스케줄
        schedule = pd.DataFrame({
            "백신": ["종합백신", "광견병", "코로나", "켄넬코프"],
            "권장월령": [2, 3, 4, 5]
        })
        st.table(schedule)
    
    st.subheader("건강 루틴 기록")
    weight = st.number_input("체중 입력 (kg)", min_value=0.0, step=0.1)
    pee_count = st.number_input("배변 횟수 기록", min_value=0)
    
    if st.button("그래프 갱신"):
        dates = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        plt.figure(figsize=(5,3))
        plt.plot(dates, [weight], marker='o')
        plt.title("체중 기록")
        plt.ylabel("kg")
        plt.xticks(rotation=45)
        st.pyplot(plt)

# ----------------------------
# 3. 증상 Q&A 안심가이드
elif menu == "증상 Q&A 안심가이드":
    st.header("증상 Q&A 안심가이드")
    symptom = st.text_input("증상 입력")
    
    if st.button("해결 방법 확인"):
        st.write(f"입력한 증상: {symptom}")
        st.info("자가처치 금지 / 위험 신호 / 즉시 내원 기준 안내 (예시)")

# ----------------------------
# 4. 동물병원 & 보험 비교 + 지도
elif menu == "동물병원 & 보험 비교":
    st.header("동물병원 & 보험 비교")
    
    # 지도용 예시 데이터
    data = {
        "병원명": ["서울동물병원1", "서울동물병원2", "서울동물병원3"],
        "주소": ["강남구", "송파구", "마포구"],
        "위도": [37.4979, 37.5142, 37.5563],
        "경도": [127.0276, 127.1056, 126.9227]
    }
    df = pd.DataFrame(data)
    
    st.subheader("내 위치 입력")
    my_lat = st.number_input("위도", value=37.5665)
    my_lon = st.number_input("경도", value=126.9780)
    
    # 지도 레이어
    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        get_position=["경도", "위도"],
        get_color=[255, 0, 0, 160],
        get_radius=200,
        pickable=True
    )
    my_layer = pdk.Layer(
        "ScatterplotLayer",
        pd.DataFrame({"lat":[my_lat],"lon":[my_lon]}),
        get_position=["lon","lat"],
        get_color=[0,0,255,200],
        get_radius=300
    )
    
    view_state = pdk.ViewState(
        latitude=my_lat,
        longitude=my_lon,
        zoom=11,
        pitch=0
    )
    
    r = pdk.Deck(
        layers=[layer, my_layer],
        initial_view_state=view_state,
        tooltip={"text":"{병원명}\n{주소}"}
    )
    st.pydeck_chart(r)
    
    # 보험 비교 예시
    st.subheader("보험 비교 (예시 데이터)")
    insurance = pd.DataFrame({
        "보험사": ["A사","B사","C사"],
        "보장 범위": ["질병, 상해","질병","상해, 질병"],
        "자기부담률": ["10%","20%","15%"]
    })
    st.table(insurance)

# ----------------------------
# 5. 커뮤니티
elif menu == "커뮤니티":
    st.header("커뮤니티")
    
    # 게시글 리스트 예시
    if 'posts' not in st.session_state:
        st.session_state['posts'] = []
    
    post_input = st.text_area("게시글 작성")
    if st.button("게시글 올리기"):
        if post_input.strip():
            st.session_state.posts.append({"text": post_input, "comments": [], "hearts": 0})
    
    for idx, post in enumerate(reversed(st.session_state.posts)):
        st.write(f"📌 {post['text']}")
        if st.button(f"❤️ {post['hearts']} 누르기", key=f"heart_{idx}"):
            post['hearts'] += 1
        comment_input = st.text_input("댓글 작성", key=f"comment_{idx}")
        if st.button("댓글 등록", key=f"comment_btn_{idx}"):
            if comment_input.strip():
                post['comments'].append(comment_input)
        for comment in post['comments']:
            st.write(f"💬 {comment}")
