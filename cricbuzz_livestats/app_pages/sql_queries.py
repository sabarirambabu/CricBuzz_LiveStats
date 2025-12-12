import streamlit as st
import pandas as pd
from utils.db_connection import get_connection


def show():
    st.title("📊 SQL Analytics")

    queries = {
        "Players from India": "SELECT playerName, role, battingStyle, bowlingStyle FROM indian_players",
        "Recent Matches": "SELECT * FROM recent_matches ORDER BY startDate DESC LIMIT 20",
        "Most Runs ODI": "SELECT * FROM mostruns_odi"
    }

    choice = st.selectbox("Choose Query", queries.keys())

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(queries[choice])
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]

    df = pd.DataFrame(rows, columns=cols)
    df.index += 1

    st.dataframe(df, width="stretch")
    conn.close()
