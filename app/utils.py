import streamlit as st


def update_st_state(key, val):
    st.session_state[key] = val
