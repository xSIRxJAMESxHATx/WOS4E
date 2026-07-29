"""SQLite persistence layer — all data is isolated per user_id."""
import sqlite3
import json
import os
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "wos4e.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS user_data (
                user_id INTEGER PRIMARY KEY,
                profile TEXT,
                plan TEXT,
                plan_type TEXT DEFAULT 'strength',
                plan_label TEXT DEFAULT 'Custom Plan',
                workout_log TEXT,
                body_log TEXT,
                nutrition_log TEXT,
                journal TEXT,
                chat_history TEXT,
                updated_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )
        conn.commit()


@contextmanager
def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def create_user(username: str, password_hash: str) -> int | None:
    try:
        with get_conn() as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, password_hash, datetime.utcnow().isoformat()),
            )
            uid = c.lastrowid
            c.execute(
                "INSERT INTO user_data (user_id, profile, plan, workout_log, body_log, nutrition_log, journal, chat_history, updated_at) VALUES (?, 'null', '[]', '[]', '[]', '[]', '[]', '[]', ?)",
                (uid, datetime.utcnow().isoformat()),
            )
            conn.commit()
            return uid
    except sqlite3.IntegrityError:
        return None


def get_user_by_username(username: str):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        return c.fetchone()


def load_user_data(user_id: int) -> dict:
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM user_data WHERE user_id = ?", (user_id,))
        row = c.fetchone()
        if not row:
            return _empty_data()
        return {
            "profile": json.loads(row["profile"] or "null"),
            "plan": json.loads(row["plan"] or "[]"),
            "plan_type": row["plan_type"] or "strength",
            "plan_label": row["plan_label"] or "Custom Plan",
            "workout_log": json.loads(row["workout_log"] or "[]"),
            "body_log": json.loads(row["body_log"] or "[]"),
            "nutrition_log": json.loads(row["nutrition_log"] or "[]"),
            "journal": json.loads(row["journal"] or "[]"),
            "chat_history": json.loads(row["chat_history"] or "[]"),
        }


def save_user_data(user_id: int, data: dict):
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            """
            UPDATE user_data SET
                profile = ?,
                plan = ?,
                plan_type = ?,
                plan_label = ?,
                workout_log = ?,
                body_log = ?,
                nutrition_log = ?,
                journal = ?,
                chat_history = ?,
                updated_at = ?
            WHERE user_id = ?
            """,
            (
                json.dumps(data.get("profile")),
                json.dumps(data.get("plan", [])),
                data.get("plan_type", "strength"),
                data.get("plan_label", "Custom Plan"),
                json.dumps(data.get("workout_log", [])),
                json.dumps(data.get("body_log", [])),
                json.dumps(data.get("nutrition_log", [])),
                json.dumps(data.get("journal", [])),
                json.dumps(data.get("chat_history", [])),
                datetime.utcnow().isoformat(),
                user_id,
            ),
        )
        conn.commit()


def _empty_data():
    return {
        "profile": None,
        "plan": [],
        "plan_type": "strength",
        "plan_label": "Custom Plan",
        "workout_log": [],
        "body_log": [],
        "nutrition_log": [],
        "journal": [],
        "chat_history": [],
    }
