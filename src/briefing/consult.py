# Filepath: src/consult.py

import openai
from src.common.advisors import advisors
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

import streamlit as st
from src.common.advisors import advisors
import openai


def consult_advisor(news_story, advisor_key):
    """Consult an advisor and generate their opinion on a news story."""
    advisor = advisors[advisor_key]
    system_prompt = f"""
    You are {advisor['Name']}, the {advisor_key}. Your personality is: {advisor['Personality']}:
    Your expertise is: {advisor['Expertise']}.
    Your backstory: {advisor['Backstory']}
    Your motivations: {advisor['Motivations']}

    Always frame your opinions and recommendations based on these traits and goals.
    """
    user_prompt = f"""
    News story: "{news_story}"
    Based on your expertise, provide your opinion on the news story and recommend a specific action for the President to take.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if preferred
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.OpenAIError as e:
        return f"Error generating advisor response: {e}"


def consult_cabinet_member(news_story, role, details):
    """Simulate consulting with a cabinet member."""
    system_prompt = f"""
    You are {details['Name']}, the {role}. Your personality is: {details['Personality']}.
    Your expertise is: {details['Expertise']}.
    Your backstory: {details['Backstory']}
    Your motivations: {details['Motivations']}

    Always frame your opinions and recommendations based on these traits and goals.
    """
    user_prompt = f"""
    News story: "{news_story}"
    Based on your expertise, provide your opinion on the news story and recommend a specific action for the President to take.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use "gpt-3.5-turbo" if preferred
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.OpenAIError as e:
        return f"Error generating cabinet member response: {e}"


def display_advisor_details(advisor_key):
    """Display advisor details with collapsible sections for bio and backstory."""
    advisor = advisors[advisor_key]
    st.write(f"### {advisor['Name']}")
    st.write(f"**Skill**: {advisor['Skill']}")
    st.write(f"**Personality**: {advisor['Personality']}")
    st.write(f"**Expertise**: {advisor['Expertise']}")

    with st.expander("Bio Details and Backstory"):
        st.write(f"**Backstory**: {advisor['Backstory']}")
        st.write(f"**Motivations**: {advisor['Motivations']}")
        if "Secret" in advisor:
            st.write(f"**Secret**: {advisor['Secret']}")
