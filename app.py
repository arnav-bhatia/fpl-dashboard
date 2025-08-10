import streamlit as st

st.set_page_config(
    page_title='FPL Analyzer',
    layout='wide',
    initial_sidebar_state='auto',
    menu_items={
        'Github Repo': 'https://github.com/arnav-bhatia/fpl-dashboard',
        'About': 'A tool to help you choose the best players for your FPL team'
    }
)

st.title('FPL Analyzer')