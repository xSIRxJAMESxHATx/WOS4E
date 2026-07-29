"""
WOS4E — Work Out Solutions for Everyone
Streamlit edition (original implementation).
Private per-user data, local SQLite persistence, ready for GitHub + Streamlit Community Cloud.
"""
from __future__ import annotations

import io
import json
from datetime import date, datetime, timedelta

import bcrypt
import pandas as pd
import plotly.express as px
import qrcode
import streamlit as st
from PIL import Image

from utils.auth import check_password, hash_password, logout, require_login
from utils.calc import (
    bmi,
    calc_bmr,
    calc_macros,
    calc_target_calories,
    calc_tdee,
    estimate_1rm,
    volume,
)
from utils.data import CATS, EXERCISES, FOODS, PROGRAMS, ex_by_id, food_by_id
from utils.db import create_user, get_user_by_username, init_db, load_user_data, save_user_data

st.set_page_config(
    page_title="WOS4E — Work Out Solutions",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Theme / CSS  (light default + dark mode toggle)
# ---------------------------------------------------------------------------
LIGHT_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', system-ui, sans-serif; }
    h1, h2, h3 { font-weight: 700 !important; letter-spacing: -0.01em; color: #1a1a1a !important; }
    .stApp { background: #f7f6f4; color: #1a1a1a; }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e8e4df; }
    div[data-testid="stMetricValue"] { color: #c1652f !important; }
    .stButton > button {
        background: #c1652f; color: white; border: none; border-radius: 8px;
        font-weight: 600; letter-spacing: 0.01em;
    }
    .stButton > button:hover { background: #e17a3d; color: white; }
    .tip {
        background: #fff8f0; border-left: 3px solid #e0a83c;
        padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; font-size: 0.92rem;
        color: #333;
    }
    .ex-card {
        background: #fff; border: 1px solid #e8e4df; border-radius: 8px;
        padding: 10px 14px; margin-bottom: 6px;
    }
    a.yt-link { color: #c1652f; text-decoration: none; font-size: 0.85rem; font-weight: 600; }
    a.yt-link:hover { text-decoration: underline; }
</style>
"""

DARK_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', system-ui, sans-serif; }
    h1, h2, h3 { font-weight: 700 !important; letter-spacing: -0.01em; color: #f0e6d2 !important; }
    .stApp { background: #141110; color: #f0e6d2; }
    [data-testid="stSidebar"] { background: #1d1917; border-right: 1px solid #3a322c; }
    div[data-testid="stMetricValue"] { color: #e17a3d !important; }
    .stButton > button {
        background: #c1652f; color: white; border: none; border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover { background: #e17a3d; color: white; }
    .tip {
        background: #2a2420; border-left: 3px solid #e0a83c;
        padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; font-size: 0.92rem;
    }
    .ex-card {
        background: #221d1a; border: 1px solid #3a322c; border-radius: 8px;
        padding: 10px 14px; margin-bottom: 6px;
    }
    a.yt-link { color: #e17a3d; text-decoration: none; font-size: 0.85rem; font-weight: 600; }
    a.yt-link:hover { text-decoration: underline; }
</style>
"""


def apply_theme():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False
    css = DARK_CSS if st.session_state.dark_mode else LIGHT_CSS
    st.markdown(css, unsafe_allow_html=True)



# ---------------------------------------------------------------------------
# Session helpers
# ---------------------------------------------------------------------------
def ensure_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "username" not in st.session_state:
        st.session_state.username = None
    if "data" not in st.session_state:
        st.session_state.data = None
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False


def persist():
    if st.session_state.user_id and st.session_state.data is not None:
        save_user_data(st.session_state.user_id, st.session_state.data)


def refresh_data():
    if st.session_state.user_id:
        st.session_state.data = load_user_data(st.session_state.user_id)


# ---------------------------------------------------------------------------
# Auth UI
# ---------------------------------------------------------------------------
def auth_screen():
    apply_theme()
    st.title("💪 WOS4E")
    st.caption("Work Out Solutions for Everyone — private, secure, yours.")
    tab_login, tab_register = st.tabs(["Log in", "Create account"])

    with tab_login:
        u = st.text_input("Username", key="login_user")
        p = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log in", type="primary", use_container_width=True):
            row = get_user_by_username(u.strip().lower())
            if row and check_password(p, row["password_hash"]):
                st.session_state.user_id = row["id"]
                st.session_state.username = row["username"]
                st.session_state.data = load_user_data(row["id"])
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab_register:
        st.info("Your data is stored only for your account and is never shared with other users.")
        nu = st.text_input("Choose username", key="reg_user")
        np1 = st.text_input("Password (min 8 chars)", type="password", key="reg_pass1")
        np2 = st.text_input("Confirm password", type="password", key="reg_pass2")
        if st.button("Create account", type="primary", use_container_width=True):
            if len(nu.strip()) < 3:
                st.error("Username must be at least 3 characters.")
            elif len(np1) < 8:
                st.error("Password must be at least 8 characters.")
            elif np1 != np2:
                st.error("Passwords do not match.")
            else:
                uid = create_user(nu.strip().lower(), hash_password(np1))
                if uid is None:
                    st.error("Username already taken.")
                else:
                    st.success("Account created — log in above.")


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_dashboard():
    st.header("Dashboard")
    data = st.session_state.data
    profile = data.get("profile")
    today = date.today().isoformat()

    col1, col2, col3, col4 = st.columns(4)
    workouts_today = [w for w in data.get("workout_log", []) if w.get("date") == today]
    nutr = [n for n in data.get("nutrition_log", []) if n.get("date") == today]
    cal = sum(n.get("cal", 0) for n in nutr)
    protein = sum(n.get("protein", 0) for n in nutr)

    with col1:
        st.metric("Workouts today", len(workouts_today))
    with col2:
        st.metric("Calories logged", f"{int(cal)}")
    with col3:
        st.metric("Protein (g)", f"{protein:.0f}")
    with col4:
        total_sessions = len(data.get("workout_log", []))
        st.metric("All-time sessions", total_sessions)

    if profile:
        bmr = calc_bmr(profile["sex"], profile["weight_kg"], profile["height_cm"], profile["age"])
        tdee = calc_tdee(bmr, profile["activity"])
        target = calc_target_calories(tdee, profile["goal"])
        macros = calc_macros(target, profile["goal"], profile["weight_kg"])
        st.subheader("Today's targets")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Calories", f"{macros['calories']}")
        c2.metric("Protein", f"{macros['protein']} g")
        c3.metric("Carbs", f"{macros['carb']} g")
        c4.metric("Fat", f"{macros['fat']} g")
        st.progress(min(1.0, cal / macros["calories"]) if macros["calories"] else 0)
        st.caption(f"Calorie progress · BMR {int(bmr)} · TDEE {int(tdee)}")
    else:
        st.warning("Set up your **Profile** for calorie & macro targets.")

    st.subheader("Current plan")
    plan = data.get("plan", [])
    if plan:
        st.write(f"**{data.get('plan_label', 'Plan')}** ({data.get('plan_type', '')})")
        rows = []
        for r in plan:
            ex = ex_by_id(r["ex"])
            rows.append(
                {
                    "Exercise": ex["name"] if ex else r["ex"],
                    "Sets": r.get("sets"),
                    "Reps": r.get("reps"),
                    "Rest (s)": r.get("rest"),
                    "Weight": r.get("weight") or "—",
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No plan loaded. Go to **Programs** or **Builder**.")


def page_profile():
    st.header("Profile")
    data = st.session_state.data
    p = data.get("profile") or {}

    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name", value=p.get("name", ""))
        age = c2.number_input("Age", min_value=12, max_value=100, value=int(p.get("age") or 30))
        sex = c1.selectbox("Sex", ["male", "female"], index=0 if p.get("sex") != "female" else 1)
        units = c2.selectbox("Units", ["metric", "imperial"], index=0 if p.get("units") != "imperial" else 1)
        if units == "imperial":
            h_val = c1.number_input("Height (in)", value=round((p.get("height_cm") or 175) / 2.54, 1))
            w_val = c2.number_input("Weight (lb)", value=round((p.get("weight_kg") or 75) * 2.20462, 1))
            height_cm = h_val * 2.54
            weight_kg = w_val / 2.20462
        else:
            height_cm = c1.number_input("Height (cm)", value=float(p.get("height_cm") or 175))
            weight_kg = c2.number_input("Weight (kg)", value=float(p.get("weight_kg") or 75))
        activity = st.selectbox(
            "Activity level",
            ["sedentary", "light", "moderate", "active", "very_active"],
            index=["sedentary", "light", "moderate", "active", "very_active"].index(
                p.get("activity", "moderate")
            ),
        )
        goal = st.selectbox(
            "Goal",
            ["lose", "maintain", "gain", "recomp"],
            index=["lose", "maintain", "gain", "recomp"].index(p.get("goal", "maintain")),
        )
        if st.form_submit_button("Save profile", type="primary"):
            data["profile"] = {
                "name": name,
                "age": age,
                "sex": sex,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "activity": activity,
                "goal": goal,
                "units": units,
                "max_lifts": p.get("max_lifts", {}),
            }
            persist()
            st.success("Profile saved.")
            st.rerun()

    if data.get("profile"):
        pr = data["profile"]
        st.metric("BMI", bmi(pr["weight_kg"], pr["height_cm"]))

    st.subheader("Log body weight")
    bw = st.number_input("Today's weight", min_value=1.0, value=float((data.get("profile") or {}).get("weight_kg") or 75))
    if st.button("Log weight"):
        data.setdefault("body_log", []).append(
            {"date": date.today().isoformat(), "weight": bw if (data.get("profile") or {}).get("units") == "metric" else bw / 2.20462}
        )
        # also update profile weight
        if data.get("profile"):
            if data["profile"].get("units") == "imperial":
                data["profile"]["weight_kg"] = bw / 2.20462
            else:
                data["profile"]["weight_kg"] = bw
        persist()
        st.success("Logged.")
        st.rerun()

    st.subheader("1RM estimator (Epley)")
    c1, c2, c3 = st.columns(3)
    w = c1.number_input("Weight lifted", min_value=0.0, value=100.0)
    r = c2.number_input("Reps", min_value=1, max_value=20, value=5)
    est = estimate_1rm(w, int(r))
    c3.metric("Estimated 1RM", est)


def page_programs():
    st.header("Programs")
    st.caption(f"{len(PROGRAMS)} programs — load any into the Builder.")
    for key, pr in PROGRAMS.items():
        with st.expander(f"{pr['label']} · {pr['type']}"):
            for it in pr["items"]:
                ex = ex_by_id(it["ex"])
                st.write(f"- **{ex['name'] if ex else it['ex']}** — {it['sets']}×{it['reps']} (rest {it['rest']}s)")
            if st.button(f"Load “{pr['label']}”", key=f"load_{key}"):
                st.session_state.data["plan"] = [
                    {"ex": i["ex"], "sets": i["sets"], "reps": i["reps"], "rest": i["rest"], "weight": 0}
                    for i in pr["items"]
                ]
                st.session_state.data["plan_type"] = pr["type"]
                st.session_state.data["plan_label"] = pr["label"]
                persist()
                st.success("Loaded into Builder.")
                st.session_state.page = "Builder"
                st.rerun()


def page_builder():
    st.header("Workout Builder")
    data = st.session_state.data
    data["plan_label"] = st.text_input("Plan name", value=data.get("plan_label", "Custom Plan"))
    data["plan_type"] = st.selectbox(
        "Type",
        ["strength", "aerobic", "power", "plyo"],
        index=["strength", "aerobic", "power", "plyo"].index(data.get("plan_type", "strength")),
    )

    plan = data.get("plan", [])
    if plan:
        for i, row in enumerate(plan):
            ex = ex_by_id(row["ex"])
            cols = st.columns([3, 1, 1, 1, 1, 0.5])
            cols[0].write(f"**{ex['name'] if ex else row['ex']}**")
            row["sets"] = cols[1].number_input("Sets", min_value=1, value=int(row.get("sets") or 3), key=f"s{i}")
            row["reps"] = cols[2].number_input("Reps", min_value=1, value=int(row.get("reps") or 8), key=f"r{i}")
            row["rest"] = cols[3].number_input("Rest", min_value=0, value=int(row.get("rest") or 60), key=f"t{i}")
            row["weight"] = cols[4].number_input("Wt", min_value=0.0, value=float(row.get("weight") or 0), key=f"w{i}")
            if cols[5].button("✕", key=f"del{i}"):
                plan.pop(i)
                persist()
                st.rerun()
        data["plan"] = plan
        persist()

    st.subheader("Add exercise")
    names = {e["id"]: f"{e['name']} ({CATS.get(e['cat'], e['cat'])})" for e in EXERCISES}
    pick = st.selectbox("Exercise", list(names.keys()), format_func=lambda k: names[k])
    if st.button("Add to plan"):
        plan.append({"ex": pick, "sets": 3, "reps": 10, "rest": 60, "weight": 0})
        data["plan"] = plan
        persist()
        st.rerun()

    st.divider()
    if st.button("Log this workout for today", type="primary"):
        entry = {
            "id": datetime.utcnow().isoformat(),
            "date": date.today().isoformat(),
            "label": data.get("plan_label", "Workout"),
            "type": data.get("plan_type", "strength"),
            "exercises": [
                {"ex": r["ex"], "sets": r["sets"], "reps": r["reps"], "weight": r.get("weight") or 0}
                for r in plan
            ],
            "total_volume": volume(plan),
        }
        data.setdefault("workout_log", []).append(entry)
        persist()
        st.success("Workout logged!")
        st.session_state.page = "Progress"
        st.rerun()


def page_library():
    st.header("Exercise Library")
    st.caption(f"{len(EXERCISES)} exercises · click YouTube for form reference")
    q = st.text_input("Search")
    cat = st.selectbox("Category", ["all"] + list(CATS.keys()), format_func=lambda c: "All" if c == "all" else CATS[c])
    shown = 0
    for e in EXERCISES:
        if cat != "all" and e["cat"] != cat:
            continue
        if q and q.lower() not in e["name"].lower():
            continue
        shown += 1
        st.markdown(
            f'<div class="ex-card"><b>{e["name"]}</b> · {CATS.get(e["cat"], e["cat"])} · {e["equip"]} · <i>{e["muscles"]}</i>'
            f' &nbsp; <a class="yt-link" href="{e["video"]}" target="_blank" rel="noopener">▶ YouTube form</a></div>',
            unsafe_allow_html=True,
        )
    if shown == 0:
        st.info("No exercises match your filters.")


def page_nutrition():
    st.header("Nutrition")
    data = st.session_state.data
    view_date = st.date_input("Date", value=date.today()).isoformat()
    entries = [n for n in data.get("nutrition_log", []) if n.get("date") == view_date]
    total_cal = sum(e.get("cal", 0) for e in entries)
    total_p = sum(e.get("protein", 0) for e in entries)
    total_c = sum(e.get("carb", 0) for e in entries)
    total_f = sum(e.get("fat", 0) for e in entries)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calories", f"{total_cal:.0f}")
    c2.metric("Protein", f"{total_p:.0f} g")
    c3.metric("Carbs", f"{total_c:.0f} g")
    c4.metric("Fat", f"{total_f:.0f} g")

    if entries:
        st.dataframe(
            pd.DataFrame(
                [{"Food": e["name"], "g": e["grams"], "kcal": round(e["cal"]), "P": round(e["protein"], 1), "C": round(e["carb"], 1), "F": round(e["fat"], 1)} for e in entries]
            ),
            use_container_width=True,
            hide_index=True,
        )

    st.subheader("Add food")
    fname = {f["id"]: f"{f['name']} ({f['cal']} kcal/100g)" for f in FOODS}
    fid = st.selectbox("Food", list(fname.keys()), format_func=lambda k: fname[k])
    grams = st.number_input("Grams", min_value=1.0, value=100.0)
    if st.button("Add food"):
        f = food_by_id(fid)
        mult = grams / 100
        data.setdefault("nutrition_log", []).append(
            {
                "id": datetime.utcnow().isoformat(),
                "date": view_date,
                "foodId": fid,
                "name": f["name"],
                "grams": grams,
                "cal": f["cal"] * mult,
                "protein": f["protein"] * mult,
                "carb": f["carb"] * mult,
                "fat": f["fat"] * mult,
            }
        )
        persist()
        st.rerun()

    # delete last
    if entries and st.button("Remove last entry for this day"):
        # remove last matching
        log = data["nutrition_log"]
        for i in range(len(log) - 1, -1, -1):
            if log[i].get("date") == view_date:
                log.pop(i)
                break
        persist()
        st.rerun()


def page_progress():
    st.header("Progress")
    data = st.session_state.data
    logs = sorted(data.get("workout_log", []), key=lambda x: x.get("date", ""))
    if logs:
        df = pd.DataFrame(
            [
                {
                    "date": l["date"],
                    "label": l.get("label"),
                    "exercises": len(l.get("exercises", [])),
                    "volume": round(l.get("total_volume") or volume(l.get("exercises", [])), 0),
                }
                for l in logs
            ]
        )
        fig = px.line(df, x="date", y="volume", markers=True, title="Training volume")
        fig.update_layout(template="plotly_dark" if st.session_state.dark_mode else "plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("No workouts logged yet.")

    bw = sorted(data.get("body_log", []), key=lambda x: x.get("date", ""))
    if bw:
        bdf = pd.DataFrame(bw)
        fig2 = px.line(bdf, x="date", y="weight", markers=True, title="Body weight (kg)")
        fig2.update_layout(template="plotly_dark" if st.session_state.dark_mode else "plotly_white")
        st.plotly_chart(fig2, use_container_width=True)


def page_journal():
    st.header("Training Journal")
    data = st.session_state.data
    text = st.text_area("How did training feel? Energy, soreness, sleep…", height=100)
    if st.button("Add entry"):
        if text.strip():
            data.setdefault("journal", []).append(
                {"id": datetime.utcnow().isoformat(), "date": date.today().isoformat(), "text": text.strip()}
            )
            persist()
            st.success("Saved.")
            st.rerun()
    entries = sorted(data.get("journal", []), key=lambda x: x.get("date", ""), reverse=True)
    for e in entries[:30]:
        st.markdown(f"**{e['date']}** — {e['text']}")


def page_recovery():
    st.header("Recovery Tips")
    profile = st.session_state.data.get("profile")
    tips_n = [
        "Prioritize protein across the day (≈1.6–2.2 g/kg) to support repair.",
        "Eat a carb + protein meal within a few hours after hard sessions.",
        "Stay hydrated — performance drops with as little as 2% body-mass fluid loss.",
    ]
    tips_r = [
        "Sleep 7–9 hours; it is the highest-leverage recovery tool.",
        "Schedule a deload every 4–6 weeks of hard training (≈40–50% volume cut).",
        "Light movement and mobility on rest days often beats complete inactivity.",
    ]
    tips_f = [
        "Progressive overload: add load, reps, or sets over time when form stays solid.",
        "Track RPE or reps-in-reserve so intensity stays intentional.",
        "Consistency beats perfection — 3 solid sessions beat 1 heroic one.",
    ]
    if profile and profile.get("goal") == "lose":
        tips_n.append("Keep a moderate deficit; very aggressive cuts impair training quality and recovery.")
    st.subheader("Nutrition")
    for t in tips_n:
        st.markdown(f'<div class="tip">{t}</div>', unsafe_allow_html=True)
    st.subheader("Recovery")
    for t in tips_r:
        st.markdown(f'<div class="tip">{t}</div>', unsafe_allow_html=True)
    st.subheader("Progression")
    for t in tips_f:
        st.markdown(f'<div class="tip">{t}</div>', unsafe_allow_html=True)


def page_share():
    st.header("Share & QR Code")
    st.caption("Generate a QR code that points people to this app (or any URL you own).")
    default_url = st.secrets.get("APP_URL", "https://share.streamlit.io/") if hasattr(st, "secrets") else "https://share.streamlit.io/"
    try:
        default_url = st.secrets["APP_URL"]
    except Exception:
        default_url = "https://YOUR-APP.streamlit.app"
    url = st.text_input("App URL to encode", value=default_url)
    if url:
        qr = qrcode.QRCode(version=1, box_size=8, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#c1652f", back_color="#141110")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption=url, width=280)
        st.download_button("Download QR PNG", buf.getvalue(), file_name="wos4e-qr.png", mime="image/png")


def page_security():
    st.header("Security & Data")
    st.markdown(
        """
- **Private by design**: every account is isolated in the database. Other users cannot read your profile, workouts, nutrition, or journal.
- **Passwords** are hashed with bcrypt (salted) — never stored in plain text.
- **Local persistence**: data is written to a SQLite file under `data/`. On Streamlit Community Cloud the filesystem is ephemeral unless you attach external storage; use **Export** below as your backup.
- This app does **not** send your training data to third parties.
        """
    )
    data = st.session_state.data
    export = json.dumps(data, indent=2)
    st.download_button("Export my data (JSON)", export, file_name="wos4e-backup.json", mime="application/json")

    uploaded = st.file_uploader("Import backup (overwrites current data)", type=["json"])
    if uploaded and st.button("Confirm import"):
        try:
            incoming = json.load(uploaded)
            st.session_state.data = incoming
            persist()
            st.success("Imported.")
            st.rerun()
        except Exception as e:
            st.error(f"Import failed: {e}")

    st.divider()
    if st.button("Log out", type="primary"):
        logout()
        st.rerun()



# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    init_db()
    ensure_state()
    apply_theme()

    if not require_login():
        auth_screen()
        return

    with st.sidebar:
        st.markdown(f"**@{st.session_state.username}**")
        st.caption("Your data stays private.")
        dark = st.toggle("Dark mode", value=st.session_state.dark_mode, key="dark_toggle")
        if dark != st.session_state.dark_mode:
            st.session_state.dark_mode = dark
            st.rerun()
        pages = [
            "Dashboard",
            "Profile",
            "Programs",
            "Builder",
            "Library",
            "Nutrition",
            "Progress",
            "Journal",
            "Recovery",
            "Share / QR",
            "Security & Data",
            ]
        choice = st.radio("Navigate", pages, index=pages.index(st.session_state.page) if st.session_state.page in pages else 0)
        st.session_state.page = choice
        st.divider()
        if st.button("Log out"):
            logout()
            st.rerun()

    page = st.session_state.page
    if page == "Dashboard":
        page_dashboard()
    elif page == "Profile":
        page_profile()
    elif page == "Programs":
        page_programs()
    elif page == "Builder":
        page_builder()
    elif page == "Library":
        page_library()
    elif page == "Nutrition":
        page_nutrition()
    elif page == "Progress":
        page_progress()
    elif page == "Journal":
        page_journal()
    elif page == "Recovery":
        page_recovery()
    elif page == "Share / QR":
        page_share()
    elif page == "Security & Data":
        page_security()


if __name__ == "__main__":
    main()
