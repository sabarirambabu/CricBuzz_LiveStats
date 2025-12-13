import streamlit as st
import pandas as pd
import requests
from utils.db_connection import HEADERS   # API headers here

# ---------------------------------
# SCORECARD FUNCTION MOVED HERE
# ---------------------------------
def get_scorecard(match_id):
    url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{match_id}/hscard"
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return {"error": str(e)}
    
def normalize_overs(overs):
    """
    Converts cricket overs like 19.6 → 20.0
    Keeps valid values like 10.4 unchanged
    """
    try:
        overs = float(overs)
        whole = int(overs)
        balls = round((overs - whole) * 10)

        if balls == 6:
            return f"{whole + 1}.0"
        else:
            return f"{whole}.{balls}"
    except:
        return overs


def show():
    st.title("🏏 LIVE Matches")

    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    res = requests.get(url, headers=HEADERS).json()

    live_matches = []

    for t in res.get("typeMatches", []):
        for series in t.get("seriesMatches", []):
            wrapper = series.get("seriesAdWrapper", {})
            matches_block = wrapper.get("matches")

            if isinstance(matches_block, list):
                iterable = matches_block
            elif isinstance(matches_block, dict):
                iterable = [matches_block]
            else:
                continue

            for m in iterable:
                info = m.get("matchInfo", {})
                score = m.get("matchScore", {})
                if not score or not isinstance(score, dict) or len(score) == 0:
                    continue

                live_matches.append({
                    "id": info.get("matchId"),
                    "teams": f"{info.get('team1', {}).get('teamName','TBD')} vs "
                             f"{info.get('team2', {}).get('teamName','TBD')}",
                    "venue": info.get("venueInfo", {}).get("ground", "N/A"),
                    "status": info.get("status", ""),
                    "scoreBlock": score
                })


    if not live_matches:
        st.error("⚠️ No live matches available.")
        return
    
    match_list = [m["teams"] for m in live_matches]
    selected = st.selectbox("Select Match", match_list)
    match = live_matches[match_list.index(selected)]

    st.markdown("### 📊 Score Overview")

    ms = match["scoreBlock"]
    rows = []

    team1_name, team2_name = match["teams"].split(" vs ")

    for tkey, tdata in ms.items():
        for ikey, inng in tdata.items():

            team_name = team1_name if "team1" in tkey else team2_name
            inning_number = int(ikey.replace("inngs", ""))

            rows.append({
                "Team": team_name,
                "InningNum": inning_number,
                "TeamOrder": 1 if team_name == team1_name else 2,
                "Score": f"{inng.get('runs','-')}/{inng.get('wickets','-')} "
                         f"({normalize_overs(inng.get('overs','-'))} ov)"
            })

    rows = sorted(rows, key=lambda x: (x["InningNum"], x["TeamOrder"]))

    df = pd.DataFrame([{"Team": r["Team"], "Score": r["Score"]} for r in rows])
    st.dataframe(df, hide_index=True, width="stretch")
    st.write(f"📢 **Status:** {match['status']}")
    st.write(f"🏟 **Venue:** {match['venue']}")

    

    st.markdown("---")
    with st.expander("📜 Show Full Scorecard"):

        scorecard = get_scorecard(match["id"])

        if "scorecard" not in scorecard:
            st.warning("⚠️ Scorecard not available.")
            return

        innings_list = scorecard["scorecard"]
        match_status = scorecard.get("status", "")

        st.markdown(f"### Match Status: **{match_status}**")

        for inng in innings_list:
            team_name = inng.get("batteamname", "Unknown")
            runs = inng.get("score", "-")
            wickets = inng.get("wickets", "-")
            overs = inng.get("overs", "-")

            st.markdown(f"#### 🏏 {team_name} – {runs}/{wickets} ({overs} ov)")

            bat_rows = [
                {
                    "Batsman": p.get("name"),
                    "Runs": p.get("runs"),
                    "Balls": p.get("balls"),
                    "4s": p.get("fours"),
                    "6s": p.get("sixes"),
                    "Strike Rate": p.get("strkrate"),
                    "Dismissal": p.get("outdec")
                }
                for p in inng.get("batsman", [])
            ]
            st.dataframe(pd.DataFrame(bat_rows), hide_index=True, width="stretch")

            bowl_rows = [
                {
                    "Bowler": p.get("name"),
                    "Overs": p.get("overs"),
                    "Runs": p.get("runs"),
                    "Wickets": p.get("wickets"),
                    "Economy": p.get("economy")
                }
                for p in inng.get("bowler", [])
            ]
            st.dataframe(pd.DataFrame(bowl_rows), hide_index=True, width="stretch")
