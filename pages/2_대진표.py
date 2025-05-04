from PIL import Image
import streamlit as st

st.set_page_config(layout="wide")

img = Image.open("bracket.png")

# 이미지 원본 크기 유지 + 가로 스크롤을 위해 container 너비 사용 안함
st.image(img, caption="🏆 토너먼트 대진표", use_container_width=False)

# 안내 메시지
st.caption("※ 이미지가 크면 좌우로 스크롤하여 확인하세요.")
