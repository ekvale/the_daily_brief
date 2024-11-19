import streamlit as st
from src.config.rss_feeds import fetch_rss_feed, RSS_FEEDS
from src.briefing.consult import consult_advisor, consult_cabinet_member
from src.common.advisors import advisors


def render_morning_briefing(rss_feeds, cabinet_members):
    """Render the Morning Briefing tab."""
    st.title("Morning Briefing")
    st.write("Stay updated on critical issues and consult with your advisors and cabinet members.")

    # Display categories in expanders
    for category, feeds in rss_feeds.items():
        with st.expander(category.replace("_", " ").title(), expanded=True):
            display_category_with_advisors_and_cabinet(category, feeds, cabinet_members)


def display_category_with_advisors_and_cabinet(category, feeds, cabinet_members):
    """Display RSS feed headlines and options to consult advisors and cabinet members for a category."""
    # Initialize session state for story index
    if f"{category}_story_index" not in st.session_state:
        st.session_state[f"{category}_story_index"] = 0

    # Compile all stories for the category
    all_stories = []
    for feed_url in feeds:
        try:
            feed_entries = fetch_rss_feed(feed_url)
            all_stories.extend(feed_entries)
        except Exception as e:
            st.error(f"Error fetching feed for {category}: {e}")

    if not all_stories:
        st.warning(f"No stories available for {category}.")
        return

    # Get the current story index and display it
    current_index = st.session_state[f"{category}_story_index"]
    story = all_stories[current_index]

    st.markdown(f"### {story['title']}")
    st.markdown(f"[Read full story]({story['link']})")

    # Navigation: Next Story Button
    if st.button(f"Next Story ({category})"):
        if current_index < len(all_stories) - 1:
            st.session_state[f"{category}_story_index"] += 1
        else:
            st.warning("No more stories available.")

    # Allow consultation with advisors and cabinet members
    st.subheader("Consultation Options")
    display_advisor_and_cabinet_dropdowns(story['title'], category, cabinet_members)


def display_advisor_and_cabinet_dropdowns(news_story, category, cabinet_members):
    """Display dropdowns for advisor and cabinet member selection and consult buttons."""
    # Advisors dropdown
    category_advisors = get_advisors_for_category(category)
    advisor_options = {key: details["Name"] for key, details in category_advisors.items()}

    selected_advisor_key = st.selectbox(
        "Select an advisor to consult",
        options=list(advisor_options.keys()),
        format_func=lambda key: advisor_options[key],
        key=f"advisor_dropdown_{category}"
    )

    # Cabinet Members dropdown
    selected_cabinet_member = st.selectbox(
        "Select a cabinet member to consult",
        options=["Select a Cabinet Member"] + list(cabinet_members.keys()),
        key=f"cabinet_dropdown_{category}"
    )

    # Consult Advisor Button
    if st.button("Consult Advisor", key=f"consult_advisor_button_{category}"):
        if selected_advisor_key:
            consultation_result = consult_advisor(news_story, selected_advisor_key)
            st.success(consultation_result)
        else:
            st.warning("Please select an advisor to consult.")

    # Consult Cabinet Member Button
    if st.button("Consult Cabinet Member", key=f"consult_cabinet_button_{category}"):
        if selected_cabinet_member != "Select a Cabinet Member":
            consultation_result = consult_cabinet_member(news_story, selected_cabinet_member, cabinet_members[selected_cabinet_member])
            st.success(consultation_result)
        else:
            st.warning("Please select a cabinet member to consult.")


def get_advisors_for_category(category):
    """Retrieve advisors relevant to a category, including Proponent and Opponent advisors."""
    category_mapping = {
        "national_security": ["Secret Advisor", "Political Advisor (Classic)", "The Constitutional Scholar", "Cowboy Curt"],
        "domestic_affairs": ["Economic Advisor", "Political Advisor (Humanitarian Visionary)", "The Constitutional Scholar", "Cowboy Curt"],
        "international_relations": ["Political Advisor (Modern)", "Political Advisor (Diplomatic Genius)", "The Constitutional Scholar", "Cowboy Curt"],
    }
    advisor_keys = category_mapping.get(category, [])
    # Always include Proponent and Opponent Advisors
    advisor_keys.extend(["Proponent Advisor", "Opponent Advisor"])
    return {key: advisors[key] for key in advisor_keys if key in advisors}
