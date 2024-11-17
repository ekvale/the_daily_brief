import streamlit as st
from src.predictions.prediction_db import get_active_predictions, submit_user_guess


def user_tab():
    st.title("Prediction Game: Make Your Guesses")

    # Input for username
    username = st.text_input("Enter your username:", "")

    # Ensure the user submits a valid username
    if not username:
        st.warning("Please enter a username to continue.")
        return

    # Display active predictions
    st.subheader("Active Predictions")
    active_predictions = get_active_predictions()

    if not active_predictions:
        st.info("No active predictions available. Check back later!")
        return

    for prediction in active_predictions:
        st.write(f"**Prediction #{prediction[0]}**: {prediction[1]}")  # Display prediction text
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Will Happen (#{prediction[0]})"):
                submit_user_guess(username, prediction[0], True)
                st.success(f"Your guess for Prediction #{prediction[0]} has been submitted!")
        with col2:
            if st.button(f"Won't Happen (#{prediction[0]})"):
                submit_user_guess(username, prediction[0], False)
                st.success(f"Your guess for Prediction #{prediction[0]} has been submitted!")
