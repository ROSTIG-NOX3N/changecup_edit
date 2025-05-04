import streamlit as st
import pandas as pd

results_df = pd.read_csv("Book(Result).csv")

st.set_page_config(layout="wide")
st.title("📋 아침체인지컵 경기 결과")

for _, match in results_df.iterrows():
    경기번호 = match['경기']
    팀1 = match['1팀']
    팀2 = match['2팀']
    팀1득점 = match['1팀득점']
    팀2득점 = match['2팀득점']
    결과 = match['결과']
    조 = match['조']
    경기일자 = match['경기일자']

    # 예정 경기 여부 판단
    is_scheduled = not (str(팀1득점).isdigit() and str(팀2득점).isdigit())

    # 카드 색상 설정
    card_color = "#f5f5f5" if not is_scheduled else "#e0e0e0"

    st.markdown(f"""
    <div style="
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        background-color: {card_color};
    ">
        <h4 style="margin-bottom: 8px;">⚽ 경기 {경기번호} | <span style='color: #007ACC;'>{조}조</span></h4>
        <p style="font-size: 18px; margin: 4px 0;">
            <strong>{팀1}</strong> {'-' if is_scheduled else f'{팀1득점}'} : {'-' if is_scheduled else f'{팀2득점}'} <strong>{팀2}</strong>
        </p>
        <p style="margin: 4px 0;">📅 <strong>경기일자:</strong> {경기일자}</p>
        <p style="margin: 4px 0;">📌 <strong>결과:</strong> {'⏳ 경기 예정' if is_scheduled else 결과}</p>
    </div>
    """, unsafe_allow_html=True)
