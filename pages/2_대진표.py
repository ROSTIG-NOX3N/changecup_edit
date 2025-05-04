from PIL import Image
import streamlit as st

st.set_page_config(layout="wide")

img = Image.open("bracket.png")

# 원본 크기 그대로 출력하고 스크롤은 Streamlit이 처리
st.image(img, caption="🏆 토너먼트 대진표", use_column_width=False)
