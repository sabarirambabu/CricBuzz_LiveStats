import os
import mysql.connector

# --------------------------------------
# LOAD SENSITIVE VALUES FROM ENVIRONMENT
# --------------------------------------

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

RAPID_API_KEY = os.getenv("RAPID_API_KEY")

HEADERS = {
    "x-rapidapi-key": RAPID_API_KEY,
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

# -----------------------------
# SQL CONNECTION FUNCTION
# -----------------------------
def get_connection():
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Exception as e:
        print("Database connection failed:", str(e))
        return None

