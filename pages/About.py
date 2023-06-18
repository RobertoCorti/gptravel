import streamlit as st

st.set_page_config(page_title="GPTravel", page_icon="✈️")

st.title("About")

st.markdown("""
GPTravel is a Web App that generates a travel plan based on Large-Language Models (LLMs). It helps users create personalized itineraries giving the best destinations, activities, and routes.

This is a simple web app that uses the power of Large Language Models to help you plan your next trip. By leveraging the GPT API, the app generates a personalized itinerary for your trip based on your destination.
To use the app, simply fill out the form on the Home page with your travel details and let GPT do the rest. You'll receive a customized travel plan that includes recommended destinations, activities, accommodations, and other useful information.
Whether you're an experienced traveler or just looking for some inspiration, this app is a fun and easy way to explore new places and ideas. So why not give it a try and see where your next journey takes you?

### Authors
- Roberto Corti 
- Stefano Polo
""", unsafe_allow_html=True)
