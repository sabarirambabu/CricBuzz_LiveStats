import streamlit as st
import pandas as pd
from utils.db_connection import get_connection


def show():
    st.title("📊 SQL Analytics")

    queries = {
        "Q1. Find all players who represent India":
            "select playerName, role as playingRole, battingStyle, bowlingStyle from indian_players",

        "Q2. Show all cricket matches played in the last few days":
        "select concat(matchDesc, ' - ', seriesName) as MatchDescription, concat(team1, ' vs ', team2) as Teams, venue as Venue, city as City, startDate as Match_Date from recent_matches order by startDate desc",

        "Q3. List the top 10 highest run scorers in ODI cricket":
        "select * from mostruns_odi",

        "Q4. Display all cricket venues with capacity > 30000":
        "select * from venue_details",

        "Q5. Calculate how many matches each team has won":
        "select concat(team , '-' , FullName) as Team, MatchesWon from matches_won_list order by MatchesWon desc",

        "Q6. Count how many players belong to each role":
        "select * from all_players",

        "Q7. Highest individual batting score in each format":
        "select * from highest_scores",

        "Q8. Show all cricket series that started in 2024":
        "select series_name, host_country, matchFormat, startDate from series_details_2024",

        "Q9. All-rounders with 1000+ runs AND 50+ wickets":
        "select * from allrounder_stats",

        "Q10. Last 20 completed matches":
        "select * from last_20_matches_table order by StartDate desc limit 20",

        "Q11. Compare player performance across formats":
        "select * from batting_stats",

        "Q12. Final results table":
        "select * from final_results0",

        "Q13. Batting partnerships scoring 100+ runs":
        "select * from partnerships_100",

        "Q14. Bowling performance at different venues (example: Bumrah)":
        "select sum(wickets) as wickets, avg(economy) as avg_economy, ground, count(ground) as matches_played from bumrah_table group by ground",
        #select sum(wickets) as wickets, avg(economy) as avg_economy, ground, count(ground) as matches_played from starc_table group by ground;
        "Q15. Players in close matches – batting impact":
        "select name, sum(total_runs) as Total_Runs, sum(innings) as Matches, sum(total_runs)/sum(innings) as Avg_Runs, sum(matches_won) as Matches_Won, sum(matches_when_batted) from close_match_stats group by name",

        "Q16. Batting performance since 2020 (yearly averages)":
        "select pid as Player_ID, name as Player_Name, year as Year, total_runs as Total_Runs, avg_runs_per_match as Avg_Runs, avg_sr as Strike_Rate, matches as Matches_Played from rr_batt_stats order by pid, year",

        "Q17. Toss advantage analysis":
        "select * from rr_toss_data",

        "Q18. Most economical bowlers in limited overs (AUS example)":
        "select player_id, (min(name)) as name, sum(runs) as total_runs, sum(balls) as total_balls, sum(runs)/sum(balls) as economy, sum(wickets) as total_wickets, min(game_format) as game_format from aus_bowl_stats group by player_id",

        "Q19. Most consistent batsmen – standard deviation":
        "select * from aus_std_deviation",

        "Q20. Matches per format + batting averages":
        "select * from all_format_batt_stats",

        "Q21. Player ranking system (batting + bowling + fielding)":
        "select * from player_points_table",

        "Q22. Head-to-head match prediction analysis":
        "select * from csk_mi_h2h",

        "Q23. Recent form & momentum for players":
        "select * from csk_batt_table",

        "Q24. Successful batting partnerships":
        "select rank() over (order by (avg_runs * 0.35 + fifty_plus_partnerships * 8 + highest_partnership * 0.2 + success_rate_percent * 0.25 + total_partnerships * 2) desc) as partnership_rank, player1_id, player1_name, player2_id, player2_name, total_partnerships, avg_runs, fifty_plus_partnerships, highest_partnership, success_rate_percent from partnership_summary order by partnership_rank",

        "Q25. Time-series analysis of career phase":
        "select name, AVG(avg_runs) AS avg_runs, AVG(avg_sr) AS avg_sr, career_phase from career_phase group by name, career_phase"
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
