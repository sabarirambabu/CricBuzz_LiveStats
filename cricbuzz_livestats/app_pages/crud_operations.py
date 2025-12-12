import streamlit as st
import pandas as pd
from utils.db_connection import get_connection


def show():
    st.title("🛠 CRUD Operations")

    conn = get_connection()
    cur = conn.cursor()

    mode = st.radio("Action", ["Create", "Read", "Update", "Delete"])

    # Create
    if mode == "Create":
        name = st.text_input("Player Name")
        team = st.text_input("Team")
        runs = st.text_input("Runs")
        wickets = st.text_input("Wickets")

        if st.button("Add"):
            cur.execute(
                "INSERT INTO players(name, team, runs, wickets) VALUES(%s, %s, %s, %s)",
                (name, team, runs, wickets)
            )
            conn.commit()
            st.success("Player added!")

    # Read
    if mode == "Read":
        cur.execute("SELECT * FROM players")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns=[col[0] for col in cur.description])
        df.index += 1
        st.dataframe(df, width="stretch")

    conn.close()
