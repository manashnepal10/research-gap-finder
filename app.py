import streamlit as st
from frontend.sidebar import render_sidebar
from frontend.main_panel import render_main_panel

st.set_page_config(
    page_title="Research Gap Finder",
    page_icon="📄",
    layout="wide",
)

render_sidebar()
render_main_panel()