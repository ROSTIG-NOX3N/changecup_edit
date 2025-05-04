from PIL import Image
import streamlit as st

st.set_page_config(layout="wide")

# 이미지 열기
img = Image.open("bracket.png")

# HTML + Streamlit 조합으로 가로 스크롤 지원
st.markdown("""
    <style>
    .scroll-container {
        overflow-x: auto;
        border: 1px solid #ccc;
        padding-bottom: 10px;
    }
    .scroll-container img {
        display: block;
    }
    </style>
""", unsafe_allow_html=True)

# 이미지 표시 (base64 없이 직접 표시)
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)
st.image(img)
st.markdown('</div>', unsafe_allow_html=True)
