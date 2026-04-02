import sqlite3
import hashlib

conn = sqlite3.connect("learnova.db", check_same_thread=False)
c = conn.cursor()

# ---------------- TABLES ----------------
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT UNIQUE,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS history (
    username TEXT,
    query TEXT,
    response TEXT
)
""")

conn.commit()

# ---------------- HASH FUNCTION ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- SIGNUP ----------------
def signup_user(username, password):
    try:
        hashed = hash_password(password)
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except:
        return False

# ---------------- LOGIN ----------------
def login_user(username, password):
    hashed = hash_password(password)
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed))
    return c.fetchone()

# ---------------- SAVE HISTORY ----------------
def save_history(username, query, response):
    c.execute("INSERT INTO history VALUES (?, ?, ?)", (username, query, response))
    conn.commit()

# ---------------- GET HISTORY ----------------
def get_history(username):
    c.execute("SELECT query, response FROM history WHERE username=?", (username,))
    return c.fetchall()
