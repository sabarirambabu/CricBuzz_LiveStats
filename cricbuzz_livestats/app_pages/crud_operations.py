import streamlit as st
import pandas as pd
from utils.db_connection import get_connection


def is_valid_text(value):
    """Allow only non-empty strings"""
    return isinstance(value, str) and value.strip() != ""


def show():
    st.title("🛠 CRUD Operations")

    mode = st.radio(
        "Choose Action",
        ["Create", "Read", "Update", "Delete"],
        horizontal=True
    )

    # -----------------------------
    # CREATE
    # -----------------------------
    if mode == "Create":
        st.subheader("➕ Add Player")

        name = st.text_input("Player Name")
        team = st.text_input("Team Name")
        runs = st.number_input("Runs", min_value=0, step=1)
        wickets = st.number_input("Wickets", min_value=0, step=1)

        if st.button("Add Player"):
            # ---------- VALIDATION ----------
            if not is_valid_text(name):
                st.error("❌ Player Name must be text")
                return

            if not is_valid_text(team):
                st.error("❌ Team Name must be text")
                return

            if not isinstance(runs, int):
                st.error("❌ Runs must be an integer")
                return

            if not isinstance(wickets, int):
                st.error("❌ Wickets must be an integer")
                return
            # --------------------------------

            conn = get_connection()
            if not conn:
                st.error("Database connection failed")
                return

            cur = conn.cursor()
            cur.execute(
                "INSERT INTO players (name, team, runs, wickets) VALUES (%s, %s, %s, %s)",
                (name.strip(), team.strip(), runs, wickets)
            )
            conn.commit()
            cur.close()
            conn.close()

            st.success("✅ Player added successfully!")

    # -----------------------------
    # READ
    # -----------------------------
    elif mode == "Read":
        st.subheader("📄 All Players")

        conn = get_connection()
        if not conn:
            st.error("Database connection failed")
            return

        cur = conn.cursor()
        cur.execute("SELECT name, team, runs, wickets FROM players")
        rows = cur.fetchall()
        cols = [c[0] for c in cur.description]

        df = pd.DataFrame(rows, columns=cols)
        df.index += 1

        cur.close()
        conn.close()

        st.dataframe(df, width="stretch")

    # -----------------------------
    # UPDATE
    # -----------------------------
    elif mode == "Update":
        st.subheader("✏️ Update Player")

        conn = get_connection()
        if not conn:
            st.error("Database connection failed")
            return

        cur = conn.cursor()
        cur.execute("SELECT name, team, runs, wickets FROM players")
        players = cur.fetchall()

        if not players:
            st.warning("No players found")
            cur.close()
            conn.close()
            return

        player_map = {f"{p[0]} ({p[1]})": p for p in players}
        selected = st.selectbox("Select Player", list(player_map.keys()))

        old_name, old_team, old_runs, old_wickets = player_map[selected]

        name = st.text_input("Player Name", old_name)
        team = st.text_input("Team Name", old_team)
        runs = st.number_input("Runs", value=old_runs, min_value=0, step=1)
        wickets = st.number_input("Wickets", value=old_wickets, min_value=0, step=1)

        if st.button("Update Player"):
            # ---------- VALIDATION ----------
            if not is_valid_text(name):
                st.error("❌ Player Name must be text")
                return

            if not is_valid_text(team):
                st.error("❌ Team Name must be text")
                return

            if not isinstance(runs, int):
                st.error("❌ Runs must be an integer")
                return

            if not isinstance(wickets, int):
                st.error("❌ Wickets must be an integer")
                return
            # --------------------------------

            cur.execute(
                """
                UPDATE players
                SET name=%s, team=%s, runs=%s, wickets=%s
                WHERE name=%s AND team=%s
                """,
                (name.strip(), team.strip(), runs, wickets, old_name, old_team)
            )
            conn.commit()
            st.success("✅ Player updated successfully!")

        cur.close()
        conn.close()

    # -----------------------------
    # DELETE
    # -----------------------------
    elif mode == "Delete":
        st.subheader("🗑 Delete Player")

        conn = get_connection()
        if not conn:
            st.error("Database connection failed")
            return

        cur = conn.cursor()
        cur.execute("SELECT name, team FROM players")
        players = cur.fetchall()

        if not players:
            st.warning("No players available")
            cur.close()
            conn.close()
            return

        player_map = {f"{p[0]} ({p[1]})": p for p in players}
        selected = st.selectbox("Select Player to Delete", list(player_map.keys()))
        name, team = player_map[selected]

        if st.button("Delete Player"):
            cur.execute(
                "DELETE FROM players WHERE name=%s AND team=%s",
                (name, team)
            )
            conn.commit()
            st.error("❌ Player deleted")

        cur.close()
        conn.close()
