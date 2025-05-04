from PIL import Image
import streamlit as st
import base64
from io import BytesIO

# 이미지 열기
img = Image.open('bracket.png')

st.set_page_config(layout="wide")

# 이미지를 메모리 버퍼에 저장하고 base64로 인코딩
buffered = BytesIO()
img.save(buffered, format="PNG")
img_b64 = base64.b64encode(buffered.getvalue()).decode()

# HTML을 이용해 스크롤 가능한 큰 이미지로 출력
st.markdown(
    f"""
    <div style="overflow-x: auto; border: 1px solid #ccc">
        <img src="data:image/png;base64,{img_b64}" style="min-width:1000px;">
    </div>
    """,
    unsafe_allow_html=True
)
