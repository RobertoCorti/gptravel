from gptravel.prototype.pages import home as home_page
import streamlit as st

st.set_page_config(page_title="GPTravel", page_icon="✈️")

if __name__ == "__main__":
    home_page.main()