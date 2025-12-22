import streamlit as st
import pandas as pd
import requests
from utils.db_connection import HEADERS


# -----------------------------
# PLAYER SEARCH FUNCTION
# -----------------------------
def search_players(name):
    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
    params = {"plrN": name}
    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=8).json()
        return res.get("player", [])
    except Exception:
        return []


# -----------------------------
# FETCH BATTING / BOWLING STATS
# -----------------------------
def get_batting_stats(player_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"
    try:
        return requests.get(url, headers=HEADERS, timeout=8).json()
    except Exception:
        return {"headers": [], "values": []}


def get_bowling_stats(player_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling"
    try:
        return requests.get(url, headers=HEADERS, timeout=8).json()
    except Exception:
        return {"headers": [], "values": []}


# -----------------------------
# CLEAN TABLE BUILDER
# -----------------------------
def build_stats_table(headers, values):
    if not headers or not values:
        return pd.DataFrame()

    cleaned = [row.get("values", []) for row in values]

    norm_rows = []
    for r in cleaned:
        if len(r) > len(headers):
            r = r[-len(headers):]
        elif len(r) < len(headers):
            r = r + [""] * (len(headers) - len(r))
        norm_rows.append(r)

    df = pd.DataFrame(norm_rows, columns=headers)
    df.index = df.index + 1
    return df


# -----------------------------
# PAGE UI
# -----------------------------
def show():

    st.title("🏆 Cricbuzz Top Player Stats")
    st.markdown("### 🔍 Player Search")

    # 1) User types name
    search_text = st.text_input("Search Player", placeholder="Start typing name...")

    selected_player = None

    # 2) Fetch suggestions ONLY when user types
    if search_text.strip():
        suggestions = search_players(search_text.strip())
    else:
        suggestions = []

    # 3) Build player labels
    suggestion_labels = [
        f"{p.get('name','Unknown')} ({p.get('teamName','N/A')})"
        for p in suggestions
    ]

    # 4) Show dropdown ONLY when suggestions exist
    if suggestions:
        chosen = st.selectbox(
            "Suggestions",
            suggestion_labels,
            label_visibility="collapsed"
        )

        idx = suggestion_labels.index(chosen)
        selected_player = suggestions[idx]

    # ----------------------------------------------------
    # DISPLAY PLAYER STATS
    # ----------------------------------------------------
    if selected_player:
        st.markdown("---")
        st.markdown(
            f"## 🏏 {selected_player.get('name','Unknown')} "
            f"({selected_player.get('teamName','')})"
        )
        st.markdown(f"**DOB:** {selected_player.get('dob','N/A')}")

        player_id = selected_player.get("id")

        bat_json = get_batting_stats(player_id)
        bowl_json = get_bowling_stats(player_id)

        bat_df = build_stats_table(bat_json.get("headers", []), bat_json.get("values", []))
        bowl_df = build_stats_table(bowl_json.get("headers", []), bowl_json.get("values", []))

        st.markdown("### 📈 Batting Career Stats")
        if bat_df.empty:
            st.info("No batting stats available.")
        else:
            st.dataframe(bat_df, width="stretch")

        st.markdown("### 🎯 Bowling Career Stats")
        if bowl_df.empty:
            st.info("No bowling stats available.")
        else:
            st.dataframe(bowl_df, width="stretch")

    # ----------------------------------------------------
    # TRADITIONAL TOP STATS
    # ----------------------------------------------------
    st.markdown("---")
    st.markdown("### 📌 Traditional Top Stats Ranking")

    match_type_map = {"Test": "1", "ODI": "2", "T20I": "3"}

    stat_types = {
        "Most Runs": "mostRuns",
        "Highest Scores": "highestScore",
        "Best Batting Average": "highestAvg",
        "Best Batting Strike Rate": "highestSr",
        "Most Hundreds": "mostHundreds",
        "Most Fifties": "mostFifties",
        "Most Fours": "mostFours",
        "Most Sixes": "mostSixes",
        "Most Nineties": "mostNineties",
        "Most Wickets": "mostWickets",
        "Best Bowling Average": "lowestAvg",
        "Best Bowling Innings": "bestBowlingInnings",
        "Most 5-Wicket Hauls": "mostFiveWickets",
        "Best Economy": "lowestEcon",
        "Best Bowling Strike Rate": "lowestSr"
    }

    col1, col2 = st.columns(2)
    with col1:
        selected_match_type = st.selectbox("Select Format", ["Test", "ODI", "T20I"])
    with col2:
        selected_stat = st.selectbox("Select Stat Type", list(stat_types.keys()))

    match_type_id = match_type_map[selected_match_type]
    stat_value = stat_types[selected_stat]

    url = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/topstats/0"
    params = {"statsType": stat_value, "matchType": match_type_id}

    try:
        res = requests.get(url, headers=HEADERS, params=params, timeout=8).json()
    except Exception as e:
        st.error(f"❌ API request failed: {e}")
        return

    values = res.get("values", [])
    headers = res.get("headers", [])

    if not values or not headers:
        st.warning("⚠️ No data found.")
        return

    cleaned = []
    for row in values:
        vals = row.get("values", [])
        if len(vals) > len(headers):
            vals = vals[-len(headers):]
        elif len(vals) < len(headers):
            vals += [""] * (len(headers) - len(vals))
        cleaned.append(vals)

    df = pd.DataFrame(cleaned, columns=headers)
    df.index = df.index + 1

    st.dataframe(df, width="stretch")
