import streamlit as st
import pandas as pd
from video_links import video_links  # ← 이 파일이 존재해야 함

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# CSS
css = """
    <style>
    body {
        background-color: #ffffff;
        color: #000000;
        font-family: Arial, sans-serif;
    }

    @media (prefers-color-scheme: dark) {
        body {
            background-color: #121212;
            color: #ffffff;
        }
        .sidebar {
            background-color: #1f1f1f;
            color: #ffffff;
        }
        .button {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff;
        }
        input, select, textarea {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
        }
        .chart {
            background-color: #222222;
            color: #ffffff;
        }
        .card {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
        }
        .highlight {
            color: #ff9800;
        }
    }

    @media (prefers-color-scheme: light) {
        body {
            background-color: #ffffff;
            color: #000000;
        }
        .sidebar {
            background-color: #f4f4f4;
            color: #000000;
        }
        .button {
            background-color: #e0e0e0;
            color: #000000;
            border: 1px solid #cccccc;
        }
        .card {
            background-color: #f9f9f9;
            color: #000000;
            border: 1px solid #ddd;
        }
    }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

# 제목
st.title("⚽ 2025 아침체인지컵 ")

def sort_key(class_name):
    grade, ban = class_name.split('학년 ')
    grade = int(grade)
    ban = int(ban.replace('반', ''))
    return grade * 10 + ban

class_stats_df["sort_order"] = class_stats_df["학반"].apply(sort_key)

# 사이드 메뉴
option = st.sidebar.selectbox(
    'Menu',
    ("메인 메뉴", "득점자", "반별 통계", "경기영상", "조별결과")
)

# 득점자 카드 스타일 함수
def scorer_card(name, team, goals, medal_color):
    medal_html = ""
    if medal_color == 'gold':
        medal_html = "<span style='color: gold;'>🥇</span>"
    elif medal_color == 'silver':
        medal_html = "<span style='color: silver;'>🥈</span>"
    elif medal_color == 'bronze':
        medal_html = "<span style='color: #cd7f32;'>🥉</span>"

    card_html = f"""
    <style>
    .scorer-card {{
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
        background-color: #f5f5f5;
        color: #000;
    }}

    @media (prefers-color-scheme: dark) {{
        .scorer-card {{
            background-color: #222;
            color: #fff;
            border: 1px solid #555;
        }}
    }}
    </style>

    <div class="scorer-card">
        <h4 style="margin: 0;">{medal_html} {name} ({team})</h4>
        <p style="margin: 0;">⚽ 득점 수: <strong>{goals}골</strong></p>
    </div>
    """
    return card_html

# 각 메뉴에 대한 분기
if option == "메인 메뉴":
    tabs = st.tabs(["본선 진출 현황"])
    with tabs[0]:
        st.subheader("본선 진출 현황")

        st.markdown("""
            <style>
            .group-box {
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
                background-color: #f0f2f6;
                border: 1px solid #ccc;
            }
            .group-box h4 { margin: 0; }
            .qualified {
                color: white;
                background-color: #28a745;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 0.9em;
            }
            .pending {
                color: #555;
                background-color: #eaeaea;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 0.9em;
            }
            @media (prefers-color-scheme: dark) {
                .group-box { background-color: #2a2a2a; border: 1px solid #444; }
                .pending { background-color: #444; color: #ccc; }
                .qualified { background-color: #28a745; color: white; }
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<div class='group-box'><h4>A조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)
        st.markdown("<div class='group-box'><h4>B조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)
        st.markdown("<div class='group-box'><h4>C조 : <span class='qualified'>2학년 2반</span></h4></div>", unsafe_allow_html=True)
        st.video("https://youtu.be/ZPLiaRIAfhg")
        st.markdown("<div class='group-box'><h4>D조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)

elif option == "득점자":
    st.subheader("다득점자")
    sorted_scorers = scorers_df.sort_values(by='득점', ascending=False)
    max_goals = sorted_scorers['득점'].max()

    for _, row in sorted_scorers.iterrows():
        if row['득점'] >= 2:
            if row['득점'] == max_goals:
                medal_color = 'gold'
            elif row['득점'] == max_goals - 1:
                medal_color = 'silver'
            elif row['득점'] == max_goals - 2:
                medal_color = 'bronze'
            else:
                medal_color = ''
            st.markdown(scorer_card(row['이름'], row['소속'], row['득점'], medal_color), unsafe_allow_html=True)

elif option == "반별 통계":
    st.markdown("### 📋 반별 경기 통계")
    col1, col2 = st.columns(2)
    with col1:
        grade = st.selectbox("학년 선택", [1, 2, 3])
    with col2:
        classroom = st.selectbox("반 선택", [1, 2, 3, 4, 5, 6, 7])
    selected_class = f"{grade}학년 {classroom}반"
    class_data = class_stats_df[class_stats_df["학반"] == selected_class]

    if not class_data.empty:
        st.markdown(f"#### 🔍 {selected_class} 경기 데이터")
        st.dataframe(class_data.reset_index(drop=True))
        wins = int(class_data['승'].sum())
        draws = int(class_data['무'].sum())
        losses = int(class_data['패'].sum())
        goals = int(class_data['득점'].sum())
        conceded = int(class_data['실점'].sum())
        goal_diff = goals - conceded
        points = wins * 3 + draws
        st.success(f"✅ **승리**: {wins} 승")
        st.warning(f"🤝 **무승부**: {draws} 무")
        st.error(f"❌ **패배**: {losses} 패")
        st.success(f"⚽ **득점**: {goals} 득점")
        st.error(f"🛡️ **실점**: {conceded} 실점")
        st.info(f"🧮 **골득실**: {goal_diff} 점")
        st.info(f"🏅 **승점**: {points} 점")

        st.markdown(f"#### 🔝 {selected_class} 득점자")
        class_scorers = scorers_df[scorers_df['소속'] == selected_class]

        if not class_scorers.empty:
            class_scorers = class_scorers.sort_values(by='득점', ascending=False)
            max_goals = class_scorers['득점'].max()

            for _, row in class_scorers.iterrows():
                if row['득점'] == max_goals:
                    medal_color = 'gold'
                elif row['득점'] == max_goals - 1:
                    medal_color = 'silver'
                elif row['득점'] == max_goals - 2:
                    medal_color = 'bronze'
                else:
                    medal_color = ''
                st.markdown(scorer_card(row['이름'], row['소속'], row['득점'], medal_color), unsafe_allow_html=True)
        else:
            st.warning("⚠️ 해당 반의 득점자 정보가 없습니다.")

elif option == "경기영상":
    st.markdown("### 🎥 경기 영상")
    for title, link in video_links.items():
        st.markdown(f"""
            <div class="video-card">
                <a href="{link}" target="_blank" class="video-title">▶ {title} 경기 영상</a>
            </div>
        """, unsafe_allow_html=True)

elif option == "조별결과":
    st.markdown("### 🏆 조별 결과")
    class_stats_df["승점"] = class_stats_df["승"] * 3 + class_stats_df["무"]
    class_stats_df["골득실"] = class_stats_df["득점"] - class_stats_df["실점"]

    def highlight_qualified(row):
        return ['background-color: green'] * len(row) if row["학반"] == "2학년 2반" else [''] * len(row)

    for group, group_data in class_stats_df.groupby("조"):
        st.markdown(f"#### 조 {group}")
        sorted_group = group_data.sort_values(
            by=["승점", "골득실", "득점", "실점"],
            ascending=[False, False, False, True]
        )
        st.dataframe(
            sorted_group[["학반", "승", "무", "패", "득점", "실점", "승점", "골득실"]]
            .style.apply(highlight_qualified, axis=1)
        )
