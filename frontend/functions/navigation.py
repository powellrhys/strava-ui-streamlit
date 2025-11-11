# Import dependencies
import streamlit as st

def get_navigation() -> st.navigation:
    """
    Function to configure application navigation and connections between pages

    Return:
        nav (st.navigation()): Streamlit navigation object
    """
    # Construct pages dictionary
    pages = [
        st.Page("pages/home.py", title="Home"),
        st.Page("pages/activities.py", title="Activity Overview"),
        st.Page("pages/heatmap.py", title="Strava Heatmap"),
        st.Page("pages/progress.py", title="Progress Overview"),
        st.Page("pages/coastal_path.py", title='Coastal Path')
    ]

    # Construct streamlit navigation object
    nav = st.navigation(pages)

    return nav
