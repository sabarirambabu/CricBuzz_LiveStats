import os
import sys
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import streamlit as st

import app_pages.home as home
import app_pages.live_matches as live
import app_pages.top_stats as stats
import app_pages.sql_queries as sql
import app_pages.crud_operations as crud

st.set_page_config(page_title="Cricbuzz LiveStats Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.markdown(
    """
    <div style="
        text-align: center;
        font-size: 49px;
        font-weight: 700;
        line-height: 40px;
    ">
        🏏<br>
        CricBuzz <br>
        LiveStats<br><br><br>
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "Go to",
    ["Home", "Live Matches", "Top Player Stats", "SQL Analytics", "CRUD Operations"]
)

if page == "Home":
    home.show()

elif page == "Live Matches":
    live.show()

elif page == "Top Player Stats":
    stats.show()

elif page == "SQL Analytics":
    sql.show()

elif page == "CRUD Operations":
    crud.show()
