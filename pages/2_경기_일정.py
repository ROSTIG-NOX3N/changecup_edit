import streamlit as st
import pandas as pd

results_df = pd.read_csv("Book(Result).csv")
st.set_page_config(layout="wide")
st.title("📋 아침체인지컵 경기 결과")

# 다크모드 대응 CSS
st.markdown("""
    <style>
    .match-card {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        background-color: #f5f5f5;
    }
    .match-card h4 {
        margin-bottom: 8px;
    }
    .match-card p {
        margin: 4px 0;
        font-size: 16px;
    }

    @media (prefers-color-scheme: dark) {
        .match-card {
            background-color: #1f1f1f;
            border: 1px solid #444;
            color: #eee;
        }
    }

    .scheduled {
        background-color: #e0e0e0;
    }

    @media (prefers-color-scheme: dark) {
        .scheduled {
            background-color: #2a2a2a;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 탭 2개 생성
tabs = st.tabs(["✅ 완료된 경기", "⏳ 예정된 경기"])

# 탭 1: 완료된 경기만
with tabs[0]:
    for _, match in results_df.iterrows():
        팀1득점 = match['1팀득점']
        팀2득점 = match['2팀득점']
        if str(팀1득점).isdigit() and str(팀2득점).isdigit():
            경기번호 = match['경기']
            팀1 = match['1팀']
            팀2 = match['2팀']
            결과 = match['결과']
            조 = match['조']
            경기일자 = match['경기일자']
            st.markdown(f"""
            <div class="match-card">
                <h4>⚽ 경기 {경기번호} | <span style='color: #007ACC;'>{조}조</span></h4>
                <p><strong>{팀1}</strong> {팀1득점} : {팀2득점} <strong>{팀2}</strong></p>
                <p>📅 <strong>경기일자:</strong> {경기일자}</p>
                <p>📌 <strong>결과:</strong> {결과}</p>
            </div>
            """, unsafe_allow_html=True)

# 탭 2: 예정된 경기만
with tabs[1]:
    for _, match in results_df.iterrows():
        팀1득점 = match['1팀득점']
        팀2득점 = match['2팀득점']
        if not (str(팀1득점).isdigit() and str(팀2득점).isdigit()):
            경기번호 = match['경기']
            팀1 = match['1팀']
            팀2 = match['2팀']
            조 = match['조']
            경기일자 = match['경기일자']
            st.markdown(f"""
            <div class="match-card scheduled">
                <h4>⚽ 경기 {경기번호} | <span style='color: #007ACC;'>{조}조</span></h4>
                <p><strong>{팀1}</strong> vs <strong>{팀2}</strong></p>
                <p>📅 <strong>경기일자:</strong> {경기일자}</p>
                <p>📌 <strong>결과:</strong> ⏳ 경기 예정</p>
            </div>
            """, unsafe_allow_html=True)
