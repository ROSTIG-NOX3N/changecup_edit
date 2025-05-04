import streamlit as st
import pandas as pd
from video_links import video_links
from PIL import Image
import base64
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="2025 아침체인지컵",
    page_icon="⚽",
    layout="wide"
)

# 데이터 불러오기
results_df = pd.read_csv('Book(Result).csv')
scorers_df = pd.read_csv('Book(Scorer).csv')
class_stats_df = pd.read_csv('Book(Class_Stat).csv')

# CSS 스타일링
st.markdown("""
<style>
body { background-color: #ffffff; color: #000000; font-family: Arial, sans-serif; }
@media (prefers-color-scheme: dark) {
  body { background-color: #121212; color: #ffffff; }
  .sidebar, .stSidebar { background-color: #1f1f1f; color: #ffffff; }
  .button, input, select, textarea { background-color: #333333; color: #ffffff; border: 1px solid #555555; }
  h1, h2, h3, h4, h5, h6 { color: #ffffff; }
}
.scorer-card { border: 1px solid #ddd; border-radius: 10px; padding: 12px; margin-bottom: 10px; background-color: #f5f5f5; color: #000; }
@media (prefers-color-scheme: dark) { .scorer-card { background-color: #222; color: #fff; border: 1px solid #555; } }
.group-box { border-radius: 12px; padding: 15px; margin-bottom: 10px; background-color: #f0f2f6; border: 1px solid #ccc; }
.qualified { color: white; background-color: #28a745; padding: 4px 8px; border-radius: 6px; font-size: 0.9em; }
.pending { color: #555; background-color: #eaeaea; padding: 4px 8px; border-radius: 6px; font-size: 0.9em; }
@media (prefers-color-scheme: dark) {
  .group-box { background-color: #2a2a2a; border: 1px solid #444; }
  .pending { background-color: #444; color: #ccc; }
  .qualified { background-color: #28a745; }
}
.notice-box { border-left: 4px solid #007acc; background-color: #e6f7ff; border-radius: 8px; padding: 12px; margin-bottom: 12px; }
@media (prefers-color-scheme: dark) { .notice-box { background-color: #1a1a1a; border-left-color: #61dafb; color: #ccc; } }
.match-card { border: 1px solid #ccc; border-radius: 10px; padding: 16px; margin-bottom: 12px; background-color: #f5f5f5; }
.match-card h4 { margin-bottom: 8px; }
.match-card p { margin: 4px 0; font-size: 16px; }
@media (prefers-color-scheme: dark) { .match-card { background-color: #1f1f1f; border: 1px solid #444; color: #eee; } }
.scheduled { background-color: #e0e0e0; }
@media (prefers-color-scheme: dark) { .scheduled { background-color: #2a2a2a; } }
.video-card { border: 1px solid #ccc; border-radius: 12px; padding: 12px 16px; margin-bottom: 10px; background-color: #fafafa; }
.video-title { font-size: 16px; font-weight: 600; color: #007acc; margin-bottom: 8px; }
@media (prefers-color-scheme: dark) { .video-card { background-color: #2a2a2a; border: 1px solid #444; } .video-title { color: #61dafb; } }
</style>
""", unsafe_allow_html=True)

# 제목
st.title("⚽ 2025 아침체인지컵")

# 클래스 정렬 키
def sort_key(class_name):
    grade, ban = class_name.split('학년 ')
    return int(grade) * 10 + int(ban.replace('반',''))
class_stats_df['sort_order'] = class_stats_df['학반'].apply(sort_key)

# 득점자 카드 생성 함수
def scorer_card(name, team, goals, medal_color):
    medal = {'gold':'🥇','silver':'🥈','bronze':'🥉'}.get(medal_color, '')
    return f"""
<div class='scorer-card'>
  <h4 style='margin:0;'>{medal} {name} ({team})</h4>
  <p style='margin:0;'>⚽ 득점 수: <strong>{goals}골</strong></p>
</div>
"""

# 대진표 표시 함수
def show_bracket(path='bracket.png'):
    img = Image.open(path)
    buffered = BytesIO()
    img.save(buffered, format='PNG')
    b64 = base64.b64encode(buffered.getvalue()).decode()
    st.markdown(f"""
<div style='overflow-x:auto;'>
  <img src='data:image/png;base64,{b64}' style='width:100%;height:auto;'>
</div>
""", unsafe_allow_html=True)

# 사이드바 메뉴
page = st.sidebar.selectbox(
    'Menu',
    ['메인 메뉴','경기 일정','득점자','반별 통계','경기영상','조별결과','대진표']
)

# 메인 메뉴
if page == '메인 메뉴':
    tabs = st.tabs(['공지사항','본선 진출 현황'])
    with tabs[0]:  # 공지사항 탭
        st.header('🔔 공지사항')
        st.markdown("""
        <div class='notice-box'>
          <ul style='margin:0; padding-left:20px;'>
            <li>매 경기 후 자동으로 데이터 반영 예정</li>
            <li>개선사항은 학생회 단톡으로 공지 예정</li>
          </ul>
        </div>
        """, unsafe_allow_html=True)
        st.info('📅 학사 일정')
        st.markdown("""
        <ul style='margin:0; padding-left:20px;'>
          <li>5월 8일 목요일 : 3학년 학력평가</li>
          <li>5월 13일 ~ 16일 : 2학년 수학여행</li>
          <li>5월 21일 : 체육대회</li>
        </ul>
        """, unsafe_allow_html=True)
    with tabs[1]:  # 본선 진출 현황 탭
        st.subheader('본선 진출 현황')
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
    with tabs[1]:
        st.subheader('본선 진출 현황')

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
        st.video('https://youtu.be/ZPLiaRIAfhg')
        st.markdown("<div class='group-box'><h4>D조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)
        st.markdown("<div class='group-box'><h4>E조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)
        st.markdown("<div class='group-box'><h4>F조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)
        st.markdown("<div class='group-box'><h4>G조 : <span class='pending'>미정</span></h4></div>", unsafe_allow_html=True)


elif page=='경기 일정':
    st.subheader('📅 경기 일정')
    tabs=st.tabs(['✅ 완료된 경기','⏳ 예정된 경기'])
    with tabs[0]:
        for _,m in results_df.iterrows():
            if str(m['1팀득점']).isdigit() and str(m['2팀득점']).isdigit():
                st.markdown(f"**⚽ 경기 {m['경기']} | {m['조']}조**")
                st.write(f"{m['1팀']} {m['1팀득점']} : {m['2팀득점']} {m['2팀']}")
                st.write(f"📌 결과: {m['결과']}  |  📅 {m['경기일자']}")
                st.markdown('---')
    with tabs[1]:
        for _,m in results_df.iterrows():
            if not(str(m['1팀득점']).isdigit() and str(m['2팀득점']).isdigit()):
                st.markdown(f"**⚽ 경기 {m['경기']} | {m['조']}조**")
                st.write(f"{m['1팀']} vs {m['2팀']}")
                st.write(f"📅 예정일자: {m['경기일자']}")
                st.markdown('---')

elif page=='득점자':
    st.subheader('다득점자')
    df=scorers_df.sort_values('득점',ascending=False)
    mv=df['득점'].max()
    for _,r in df.iterrows():
        if r['득점']>=2:
            medal='gold' if r['득점']==mv else 'silver' if r['득점']==mv-1 else 'bronze' if r['득점']==mv-2 else ''
            st.markdown(scorer_card(r['이름'],r['소속'],r['득점'],medal),unsafe_allow_html=True)

elif page=='반별 통계':
    st.markdown('### 📋 반별 경기 통계')
    grade=st.selectbox('학년',[1,2,3])
    ban=st.selectbox('반',[1,2,3,4,5,6,7])
    sel=f"{grade}학년 {ban}반"
    data=class_stats_df[class_stats_df['학반']==sel].reset_index(drop=True)
    if not data.empty:
        st.dataframe(data.drop(columns=['sort_order']))
        w,d,l=data['승'].sum(),data['무'].sum(),data['패'].sum()
        gf,ga=data['득점'].sum(),data['실점'].sum()
        gd,pts=gf-ga,w*3+d
        st.success(f"✅ 승리: {w}승")
        st.warning(f"🤝 무승부: {d}무")
        st.error(f"❌ 패배: {l}패")
        st.success(f"⚽ 득점: {gf}골")
        st.error(f"🛡️ 실점: {ga}실점")
        st.info(f"🧮 골득실: {gd}점")
        st.info(f"🏅 승점: {pts}점")
        sub=scorers_df[scorers_df['소속']==sel]
        if not sub.empty:
            mv2=sub['득점'].max()
            for _,r in sub.sort_values('득점',ascending=False).iterrows():
                medal='gold' if r['득점']==mv2 else 'silver' if r['득점']==mv2-1 else 'bronze' if r['득점']==mv2-2 else ''
                st.markdown(scorer_card(r['이름'],r['소속'],r['득점'],medal),unsafe_allow_html=True)
        else:
            st.warning('⚠️ 해당 반의 득점자 정보가 없습니다.')

elif page=='경기영상':
    st.subheader('🎥 경기 영상')
    for t,l in video_links.items():
        st.markdown(f"<div class='video-card'><p class='video-title'>▶ {t} 경기 영상</p></div>",unsafe_allow_html=True)
        st.video(l)

elif page=='대진표':
    st.subheader('🏆 토너먼트 대진표')
    with st.spinner('이미지를 불러오는 중입니다...'):
        show_bracket('bracket.png')
    st.caption('※ 이미지가 크면 좌우로 스크롤하여 확인하세요.')
