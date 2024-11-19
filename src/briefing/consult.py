# Filepath: src/consult.py

import openai
from src.common.advisors import advisors
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def consult_advisor(news_story, advisor_key):
    """Provide consultation based on the selected advisor and the news story."""
    # Keywords triggering special alerts for Cowboy Curt
    cowboy_keywords = [
        "Syria", "Damascus", "EMP", "Apocalypse", "Rapture", "End Times", "Revelation",
        "Judgment Day", "Prophecy", "Armageddon"
    ]

    # Check for Cowboy Curt
    if advisor_key == "Cowboy Curt":
        # Trigger an alert if any keyword is found in the news story
        for keyword in cowboy_keywords:
            if keyword.lower() in news_story.lower():
                st.warning(
                    f"⚠️ **Cowboy Curt Alert!** ⚠️\n"
                    f"This story contains references to '{keyword}', which Curt believes may "
                    f"signal divine prophecy or critical Homeland Security concerns. He advises immediate action!"
                )

        # Use GPT to generate a prepper-style response
        system_prompt = f"""
        You are Cowboy Curt, a Homeland Security operative and devout believer in divine prophecy. 
        You consider yourself the 'Special Forces of God,' with expertise in Homeland Security and preparing for apocalyptic scenarios.

        Your personality is zealous, resolute, and enigmatic. 
        Your expertise includes anticipating potential catastrophic events, such as EMP attacks, and promoting preparedness.
        Your motivations are to protect the nation while preparing for divine events such as the rapture.

        Always frame your opinions and recommendations based on these traits, focusing on actionable steps to ensure readiness.
        """
        user_prompt = f"""
        News story: "{news_story}"
        Based on your expertise, provide a prepper-focused opinion on this news story and recommend specific actions for the President to take.
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

    # Default response for other advisors
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
    You are {details['Name']}, the {role}. Your personality is: {details['Personality']}:
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
