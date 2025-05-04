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
  .sidebar { background-color: #1f1f1f; color: #ffffff; }
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
    return int(grade)*10 + int(ban.replace('반',''))
class_stats_df['sort_order'] = class_stats_df['학반'].apply(sort_key)

# 득점자 카드 함수
def scorer_card(name, team, goals, medal_color):
    medal = {'gold':'🥇','silver':'🥈','bronze':'🥉'}.get(medal_color, '')
    return f"""
<div class='scorer-card'>
  <h4 style='margin:0;'>{medal} {name} ({team})</h4>
  <p style='margin:0;'>⚽ 득점 수: <strong>{goals}골</strong></p>
</div>
"""

# 대진표 함수
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
page = st.sidebar.selectbox('Menu', ['메인 메뉴','경기 일정','득점자','반별 통계','경기영상','조별결과','대진표'])

# 메인 메뉴
if page == '메인 메뉴':
    st.subheader('본선 진출 현황')
    for grp in ['A','B','C','D','E','F','G']:
        status = 'qualified' if grp=='C' else 'pending'
        label = '2학년 2반' if grp=='C' else '미정'
        st.markdown(f"<div class='group-box'><h4>{grp}조 : <span class='{status}'>{label}</span></h4></div>", unsafe_allow_html=True)
    st.video('https://youtu.be/ZPLiaRIAfhg')

# 경기 일정
elif page == '경기 일정':
    st.subheader('📅 경기 일정')
    tabs = st.tabs(['✅ 완료된 경기','⏳ 예정된 경기'])
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

# 득점자
elif page == '득점자':
    st.subheader('다득점자')
    df = scorers_df.sort_values('득점',ascending=False)
    m = df['득점'].max()
    for _,r in df.iterrows():
        if r['득점']>=2:
            medal = 'gold' if r['득점']==m else 'silver' if r['득점']==m-1 else 'bronze' if r['득점']==m-2 else ''
            st.markdown(scorer_card(r['이름'],r['소속'],r['득점'],medal),unsafe_allow_html=True)

# 반별 통계
elif page == '반별 통계':
    st.markdown('### 📋 반별 경기 통계')
    grade = st.selectbox('학년',[1,2,3])
    ban = st.selectbox('반',[1,2,3,4,5,6,7])
    sel = f"{grade}학년 {ban}반"
    data = class_stats_df[class_stats_df['학반']==sel].reset_index(drop=True)
    if not data.empty:
        st.dataframe(data.drop(columns=['sort_order']))
        w,d,l = data['승'].sum(),data['무'].sum(),data['패'].sum()
        gf,ga = data['득점'].sum(),data['실점'].sum()
        gd,pts = gf-ga, w*3+d
        st.success(f"✅ 승리: {w}승")
        st.warning(f"🤝 무승부: {d}무")
        st.error(f"❌ 패배: {l}패")
        st.success(f"⚽ 득점: {gf}골")
        st.error(f"🛡️ 실점: {ga}실점")
        st.info(f"🧮 골득실: {gd}점")
        st.info(f"🏅 승점: {pts}점")
        sub = scorers_df[scorers_df['소속']==sel]
        if not sub.empty:
            mm = sub['득점'].max()
            for _,r in sub.sort_values('득점',ascending=False).iterrows():
                medal = 'gold' if r['득점']==mm else 'silver' if r['득점']==mm-1 else 'bronze' if r['득점']==mm-2 else ''
                st.markdown(scorer_card(r['이름'],r['소속'],r['득점'],medal),unsafe_allow_html=True)
        else:
            st.warning('⚠️ 해당 반의 득점자 정보가 없습니다.')

# 경기영상
elif page == '경기영상':
    st.subheader('🎥 경기 영상')
    for t,l in video_links.items():
        st.markdown(f"<div class='video-card'><p class='video-title'>▶ {t} 경기 영상</p></div>",unsafe_allow_html=True)
        st.video(l)

# 조별결과
elif page == '조별결과':
    st.subheader('🏆 조별 결과')
    df = class_stats_df.copy()
    df['승점']=df['승']*3+df['무']
    df['골득실']=df['득점']-df['실점']
    for grp,grp_df in df.groupby('조'):
        st.markdown(f"#### 조 {grp}")
        styled = grp_df.sort_values(['승점','골득실','득점','실점'],ascending=[False,False,False,True])
        st.dataframe(styled[['학반','승','무','패','득점','실점','승점','골득실']]
                     .style.apply(lambda r: ['background-color: green']*len(r) if r['학반']=='2학년 2반' else ['']*len(r),axis=1))

# 대진표
elif page == '대진표':
    st.subheader('🏆 토너먼트 대진표')
    show_bracket('bracket.png')
