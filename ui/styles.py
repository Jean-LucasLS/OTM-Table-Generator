import streamlit as st

_BASE_STYLE = '''
<style>
  .block-container {
    padding-top: 1.6rem;
    padding-bottom: 1.6rem;
  }
  .stSelectbox > div > div,
  .stTextInput > div > div,
  .stNumberInput > div > div {
    border-radius: 8px;
  }
  .stDownloadButton > button,
  .stFileUploader > div {
    border-radius: 8px;
  }
  .stDataFrame {
    border-radius: 8px;
    overflow: hidden;
  }
</style>
'''


def apply_basic_style():
  st.markdown(_BASE_STYLE, unsafe_allow_html=True)
