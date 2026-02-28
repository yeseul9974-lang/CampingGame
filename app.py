import streamlit as st

# 1. 점수 계산 함수 (LaTeX 수식 기반 로직)
def calculate_score(index_val):
    if index_val >= 80: return 10
    elif index_val >= 40: return 6
    elif index_val >= 20: return 4
    else: return 1

# 2. 게임 데이터 설정
game_rounds = [
    {
        "round": "1R: 커플 캠핑의 로망",
        "condition": "첫 커플 캠핑! 인스타 감성이 가장 중요한 상황에서 선택할 메인 고기는?",
        "options": {"토마호크": 100, "우대갈비": 85, "삼겹살": 55, "목살": 40, "양갈비": 30}
    },
    {
        "round": "2R: 한파 생존 국물",
        "condition": "몸이 으슬으슬 추워오는 영하 10도! 간편하면서 뜨끈한 메뉴는?",
        "options": {"어묵탕": 100, "부대찌개": 82, "김치찌개": 45, "밀푀유나베": 38, "돈코츠라멘": 15}
    },
    {
        "round": "3R: 어른들의 힐링 타임",
        "condition": "아이들은 잠들고, 어른들끼리 조용히 즐기는 본격적인 야식 안주는?",
        "options": {"감바스 알 아히요": 100, "소곱창/대창 구이": 88, "먹태/노가리": 62, "닭발": 45, "치즈 플래터": 30}
    }
]

# 3. 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.total_score = 0
    st.session_state.game_over = False

# 4. 웹 UI 구성
st.set_page_config(page_title="캠핑 트렌드 퀴즈", page_icon="🏕️")
st.title("🏕️ 캠핑 음식 트렌드 퀴즈")

# 여기에 삽입! (파일명을 실제 업로드한 이름으로 바꿔주세요)
st.image("header_camping_image.jpg", use_container_width=True) 

st.caption("대중의 선택에 얼마나 가까운지 테스트해보세요!")st.caption("대중의 선택에 얼마나 가까운지 테스트해보세요!")

if not st.session_state.game_over:
    # --- 1~3라운드 공통 진행 ---
    if st.session_state.step < 3:
        current = game_rounds[st.session_state.step]
        st.subheader(current['round'])
        st.info(current['condition'])
        
        choice = st.radio("당신의 선택은?", list(current['options'].keys()), key=f"r{st.session_state.step}")
        
        if st.button("결정하기"):
            val = current['options'][choice]
            st.session_state.total_score += calculate_score(val)
            st.session_state.step += 1
            st.rerun()

    # --- 4라운드: 상황 선택 (가족 vs 솔로) ---
    elif st.session_state.step == 3:
        st.subheader("4R: 당신의 캠핑 스타일은?")
        mode = st.radio("어떤 상황의 간식을 고르시겠어요?", ["조카들과 함께하는 가족 캠핑", "고요함을 즐기는 솔로 캠핑"])
        
        if mode == "조카들과 함께하는 가족 캠핑":
            opts = {"마시멜로": 100, "스모어 키트": 92, "구운 치즈": 75, "꿀호떡 구이": 55, "달고나": 30}
            cond = "인기 삼촌/고모가 되기 위한 필살기 디저트는?"
        else:
            opts = {"군고구마/감자": 100, "소곱창/대창 구이": 85, "구운 과일": 60, "개인용 스모어": 42, "드립 커피": 25}
            cond = "혼자만의 고요한 불멍에 어울리는 별미는?"
            
        st.write(f"**상황:** {cond}")
        choice = st.selectbox("간식을 선택하세요:", list(opts.keys()))
        
        if st.button("간식 결정!"):
            st.session_state.total_score += calculate_score(opts[choice])
            st.session_state.step += 1
            st.rerun()

    # --- 5라운드: 상황 선택 (긴박 vs 여유) ---
    elif st.session_state.step == 4:
        st.subheader("5R: 마지막 날 아침")
        time_mode = st.radio("지금 시간적 여유가 있나요?", ["퇴실 1시간 전 (긴박)", "퇴실 3시간 전 (여유)"])
        
        if time_mode == "퇴실 1시간 전 (긴박)":
            opts = {"컵라면": 100, "토스트": 65, "순두부찌개": 42, "볶음밥": 35, "누룽지": 20}
            cond = "11시 퇴실! 텐트도 아직 못 접었다. 가장 효율적인 아침은?"
        else:
            opts = {"프렌치 토스트 & 드립 커피": 100, "에그 인 헬": 85, "잉글리시 브렉퍼스트": 68, "생선구이와 솥밥": 42, "컵라면": 15}
            cond = "햇살이 따스한 아침. 가장 '나를 아끼는' 조식 메뉴는?"

        st.write(f"**상황:** {cond}")
        choice = st.selectbox("아침 식사를 선택하세요:", list(opts.keys()))
        
        if st.button("최종 선택!"):
            st.session_state.total_score += calculate_score(opts[choice])
            st.session_state.game_over = True
            st.rerun()

# 5. 결과 화면
else:
    st.balloons()
    st.header("🏆 게임 종료!")
    st.metric("당신의 최종 점수", f"{st.session_state.total_score}점")
    
    # 점수 기준표 (LaTeX)
    st.latex(r"Score = \begin{cases} 10, & \text{if } 80 \le x \le 100 \\ 6, & \text{if } 40 \le x < 80 \\ 4, & \text{if } 20 \le x < 40 \\ 1, & \text{if } 0 \le x < 20 \end{cases}")

    if st.session_state.total_score >= 45:
        st.success("🔥 **당신은 캠핑 트렌드 세터!** 사람들의 마음을 꿰뚫어 보시는군요.")
    elif st.session_state.total_score >= 30:
        st.info("🌳 **프로 캠퍼!** 대중적이고 합리적인 선택을 즐기시네요.")
    else:
        st.warning("🐣 **자유로운 영혼의 캠린이!** 유행보다는 본인만의 길을 가시네요.")

    if st.button("다시 도전하기"):
        st.session_state.clear()
        st.rerun()
