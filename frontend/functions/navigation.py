# Import dependencies
import streamlit as st

def get_navigation() -> st.navigation:
    """
    Function to configure application navigation and connections between pages

    Return:
        nav (st.navigation()): Streamlit navigation object
    """
    # Construct pages dictionary
    pages = {
        "Overview": [
            st.Page(page="pages/home.py", title="Home", icon="🏠"),
            st.Page("pages/activities.py", title="Activity Overview", icon="📊"),
            st.Page("pages/progress.py", title="Progress Overview", icon="📈"),
        ],
        "HeatMap": [
            st.Page("pages/heatmap.py", title="Strava Heatmap", icon="🌎"),
            st.Page("pages/coastal_path.py", title='Welsh Coastal Path', icon="🌊"),
            st.Page("pages/mountains.py", title='Welsh Mountain Climbing', icon="⛰️"),
        ],
        "Running": [
            st.Page("pages/pb_efforts.py", title="PB Efforts Overview", icon="🏆"),
            st.Page("pages/race_analysis.py", title="Race Analysis", icon="🏃‍♂️"),
        ],
        "Triathlon": [
            st.Page("pages/triathlon_training.py", title="Training Overview", icon="🚲"),
        ]
    }

    # Construct streamlit navigation object
    nav = st.navigation(pages)

    return nav
