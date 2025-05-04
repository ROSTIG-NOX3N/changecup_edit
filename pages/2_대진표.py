from PIL import Image 
import streamlit as st

img = Image.open('대진표.png')

st.image(img, use_container_width=True)
