import streamlit as st
from src.predictions.prediction_db import add_prediction, update_prediction_outcome, get_active_predictions


def admin_tab():
    st.title("Admin Panel: Manage Predictions")

    # Add a new prediction
    st.subheader("Add New Prediction")
    new_prediction = st.text_input("Prediction Text")
    if st.button("Add Prediction"):
        add_prediction(new_prediction)
        st.success("Prediction added successfully!")

    # Resolve predictions
    st.subheader("Resolve Predictions")
    active_predictions = get_active_predictions()
    for pred in active_predictions:
        st.write(f"Prediction #{pred[0]}: {pred[1]}")
        if st.button(f"Set Outcome to True (#{pred[0]})"):
            update_prediction_outcome(pred[0], True)
            st.success("Outcome set to True.")
        if st.button(f"Set Outcome to False (#{pred[0]})"):
            update_prediction_outcome(pred[0], False)
            st.success("Outcome set to False.")
