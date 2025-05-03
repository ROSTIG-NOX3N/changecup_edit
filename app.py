import streamlit as st
import pandas as pd
from video_links import video_links

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# 페이지 제목
st.title("⚽ 2025 아침체인지컵 ")

# CSS 파일 불러오기
st.markdown('<link rel="stylesheet" href="style.css">', unsafe_allow_html=True)

def sort_key(class_name):
    grade, ban = class_name.split('학년 ')
    grade = int(grade)
    ban = int(ban.replace('반', ''))
    return grade * 10 + ban

class_stats_df["sort_order"] = class_stats_df["학반"].apply(sort_key)

# 사이드 메뉴
option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "득점자", "반별 통계")
)

# 득점자 카드 HTML
def scorer_card(name, team, goals, medal_color):
    medal_html = ""
    if medal_color == 'gold':
        medal_html = "<span style='color: gold;'>🥇</span>"
    elif medal_color == 'silver':
        medal_html = "<span style='color: silver;'>🥈</span>"
    elif medal_color == 'bronze':
        medal_html = "<span style='color: #cd7f32;'>🥉</span>"

    card_html = f"""
    <div class="scorer-card">
        <h4 style="margin: 0;">{medal_html} {name} ({team})</h4>
        <p style="margin: 0;">⚽ 득점 수: <strong>{goals}골</strong></p>
    </div>
    """
    return card_html

if option == "메인 메뉴":
    # 탭 4개: 공지사항, 경기영상, 조별결과, 전체결과
    tab1, tab2, tab3, tab4 = st.tabs(["공지사항", "경기영상", "조별결과", "전체 결과"])

    with tab1:
        st.subheader("본선 진출 현황")
        st.markdown("<div class='group-box'><h4>A조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)
        st.markdown("<div class='group-box'><h4>B조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)
        st.markdown("<div class='group-box'><h4>C조 : <span class='qualified'>2학년 2반</span></h4></div>", unsafe_allow_html=True)
        st.video("https://youtu.be/ZPLiaRIAfhg")
        st.markdown("<div class='group-box'><h4>D조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 🎥 경기 영상")
    
        for title, link in video_links.items():
            st.markdown(f"""
            <div class="video-card">
                <a href="{link}" target="_blank" class="video-title">▶ {title}경기 영상</a>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.subheader("조별 결과")
        # 조별 결과 출력 부분 (예시 데이터 사용)
        for index, row in class_stats_df.iterrows():
            st.markdown(f"<div class='group-box'><h4>{row['학반']}: {row['승']}</h4></div>", unsafe_allow_html=True)

    with tab4:
        st.subheader("전체 결과")
        # 전체 결과 출력 부분 (예시 데이터 사용)
        for index, row in results_df.iterrows():
            st.write(f"경기: {row['경기명']} - 결과: {row['결과']}")
