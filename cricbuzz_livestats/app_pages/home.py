import streamlit as st

def show():
    st.title("🏏 Cricbuzz LiveStats")
    st.subheader("Cricket Analytics Dashboard")

    st.markdown("---")

    st.markdown("""
    ### 📌 Project Overview
    **Cricbuzz LiveStats** is an interactive cricket analytics dashboard built using  
    **Python, Streamlit, MySQL, and the Cricbuzz API**.

    The application provides:
    - 🏏 Real-time live match scores
    - 📊 Player performance statistics
    - 🗄 SQL-based analytical insights
    - ✏️ Player data management using CRUD operations
    """)

    st.markdown("---")

    st.markdown("""
    ### 🧰 Tools & Technologies Used
    - **Python**
    - **Streamlit**
    - **Pandas**
    - **Requests**
    - **MySQL**
    - **Cricbuzz API (RapidAPI)**
    - **Git & GitHub**
    """)

    st.markdown("---")

    st.markdown("""
    ### 📂 Application Pages
    - 🏠 **Home** – Project overview and instructions  
    - 🏏 **Live Matches** – Live scores, venue, and match status  
    - 📈 **Top Player Stats** – Batting and bowling leaderboards  
    - 🗄 **SQL Analytics** – 25+ advanced SQL queries  
    - ✏️ **CRUD Operations** – Manage player records  
    """)

    st.markdown("---")
    st.info("📌 Use the sidebar to navigate between different pages of the application.")
