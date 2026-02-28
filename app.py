import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. 점수 계산 함수
def calculate_score(index_val):
    if index_val >= 80: return 10
    elif index_val >= 40: return 6
    elif index_val >= 20: return 4
    else: return 1

# 2. 구글 시트 연결 설정 (랭킹 시스템용)
# 주의: 실제 배포 시에는 Streamlit Secrets에 시트 URL을 등록해야 합니다.
# 여기서는 시뮬레이션을 위해 리스트로 작동하는 로직을 포함합니다.
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 게임 데이터 설정 (기존과 동일)
game_rounds = [
    {"round": "1R: 캠핑엔 고기", "condition": "첫 캠핑! 캠핑의 꽃은 고기!",
     "options": {"양갈비": 28, "목살": 85, "우대갈비": 48, "삼겹살": 100, "토마호크": 62}},
    {"round": "2R: 생존을 위한 국물은 필수", "condition": "가만히 앉아있다 보니 몸이 으슬으슬 추워온다. 간편하면서 뜨끈한 무언가가 먹고싶은데..", 
     "options": {"김치찌개": 45, "부대찌개": 82, "돈코츠라멘": 15, "밀푀유나베": 38, "어묵탕": 100}},
    {"round": "3R: 어른들의 힐링 타임", "condition": "아이들은 잠들고, 어른들끼리 조용히 즐기는 본격적인 야식 안주는?", 
     "options": {"소곱창/대창 구이": 88, "감바스 알 아히요": 100, "먹태/노가리": 62, "닭발": 45, "치즈 플래터": 30}}
]

# 4. 세션 상태 초기화
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.total_score = 0
    st.session_state.game_over = False
    st.session_state.user_name = "" # 사용자 이름 저장

# 5. 웹 UI 구성
st.set_page_config(page_title="캠핑 트렌드 퀴즈", page_icon="🏕️")

# --- 메인 화면: 이름 입력 ---
if st.session_state.user_name == "":
    st.title("🏕️ 캠핑 트렌드 퀴즈")
    st.image("header_camping_image.jpg", use_container_width=True)
    st.subheader("게임을 시작하기 전, 이름을 알려주세요!")
    user_name = st.text_input("닉네임 입력", placeholder="예: 캠핑왕")
    if st.button("게임 시작"):
        if user_name:
            st.session_state.user_name = user_name
            st.rerun()
        else:
            st.warning("이름을 입력해야 랭킹에 등록될 수 있습니다!")
    st.stop()

st.title("🏕️ 캠핑 음식 트렌드 퀴즈")
st.caption(f"플레이어: {st.session_state.user_name}님")

if not st.session_state.game_over:
    # 1~3라운드 공통 진행 (기존 로직)
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

    # 4라운드: 가족 vs 솔로 (기존 로직)
    elif st.session_state.step == 3:
        st.subheader("4R: 당신의 캠핑 스타일은?")
        mode = st.radio("상황 선택", ["조카들과 함께하는 가족 캠핑", "고요함을 즐기는 솔로 캠핑"])
        if mode == "조카들과 함께하는 가족 캠핑":
            opts, cond = {"마시멜로": 100, "스모어 키트": 92, "구운 치즈": 75, "꿀호떡 구이": 55, "달고나": 30}, "인기 삼촌/고모가 되기 위한 필살기 디저트는?"
        else:
            opts, cond = {"군고구마/감자": 100, "소곱창/대창 구이": 85, "구운 과일": 60, "개인용 스모어": 42, "드립 커피": 25}, "혼자만의 고요한 불멍에 어울리는 별미는?"
        st.write(f"**상황:** {cond}")
        choice = st.selectbox("간식을 선택하세요:", list(opts.keys()))
        if st.button("간식 결정!"):
            st.session_state.total_score += calculate_score(opts[choice])
            st.session_state.step += 1
            st.rerun()

    # 5라운드: 긴박 vs 여유 (기존 로직)
    elif st.session_state.step == 4:
        st.subheader("5R: 마지막 날 아침")
        time_mode = st.radio("시간적 여유?", ["퇴실 1시간 전 (긴박)", "퇴실 3시간 전 (여유)"])
        if time_mode == "퇴실 1시간 전 (긴박)":
            opts, cond = {"컵라면": 100, "토스트": 65, "순두부찌개": 42, "볶음밥": 35, "누룽지": 20}, "가장 효율적인 아침은?"
        else:
            opts, cond = {"프렌치 토스트 & 드립 커피": 100, "에그 인 헬": 85, "잉글리시 브렉퍼스트": 68, "생선구이와 솥밥": 42, "컵라면": 15}, "가장 '나를 아끼는' 조식 메뉴는?"
        st.write(f"**상황:** {cond}")
        choice = st.selectbox("아침 식사를 선택하세요:", list(opts.keys()))
        if st.button("최종 선택!"):
            st.session_state.total_score += calculate_score(opts[choice])
            st.session_state.game_over = True
            st.rerun()

# --- 결과 화면 및 실시간 공유 랭킹 ---
else:
    st.balloons()
    st.header(f"🏆 {st.session_state.user_name}님 종료!")
    st.metric("최종 점수", f"{st.session_state.total_score}점")

    # 1. 등급 메시지
    if st.session_state.total_score >= 45:
        st.success("🔥 **당신은 캠핑 트렌드 세터!**")
    elif st.session_state.total_score >= 30:
        st.info("🌳 **프로 캠퍼!**")
    else:
        st.warning("🐣 **자유로운 영혼의 캠린이!**")

    st.markdown("---")
    st.subheader("🏅 전 세계 캠핑 고수 TOP 3")

    try:
        # 2. 구글 시트에서 데이터 읽기
        df = conn.read(ttl="0s") # 실시간 반영을 위해 캐시를 끕니다
        
        # 3. 이번 판 점수 추가하기
        new_data = pd.DataFrame([{"Name": st.session_state.user_name, "Score": st.session_state.total_score}])
        updated_df = pd.concat([df, new_data], ignore_index=True)
        
        # 4. 구글 시트에 업데이트 저장 (이 한 줄이 핵심!)
        conn.update(data=updated_df)
        
        # 5. 상위 3명 정렬해서 보여주기
        top_3 = updated_df.sort_values(by="Score", ascending=False).head(3)
        
        for i, row in enumerate(top_3.itertuples(), 1):
            medal = ["🥇", "🥈", "🥉"][i-1]
            st.write(f"{medal} {i}위: **{row.Name}** - {row.Score}점")
            
 # 기존 except 부분을 이렇게 잠시 바꿔보세요
except Exception as e:
    st.error(f"진짜 에러 내용: {e}") # 이렇게 하면 컴퓨터가 진짜 이유를 말해줍니다!

    if st.button("다시 도전하기"):
        st.session_state.clear()
        st.rerun()
