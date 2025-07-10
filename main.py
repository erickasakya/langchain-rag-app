import streamlit as st

retrieve_generate_chat = st.Page(
    "chat.py", title="Chat", icon=":material/chat:", default=True
)
load_split_store = st.Page("load.py", title="Load Data", icon=":material/dashboard:")

pg = st.navigation([retrieve_generate_chat, load_split_store])

pg.run()
