"""Password hashing and session helpers."""
import bcrypt
import streamlit as st


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def check_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False


def require_login():
    """Redirect-style guard: returns True if logged in."""
    return st.session_state.get("user_id") is not None


def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
