# WOS4E — Work Out Solutions for Everyone

**Private, secure fitness & nutrition tracker** built with Streamlit.

Inspired by a rich client-side workout SPA, this edition is rewritten from the ground up as an original Streamlit application so you:

- Own the full source code
- Keep every user’s data isolated and private
- Can deploy to [Streamlit Community Cloud](https://share.streamlit.io) or self-host
- Can monetize (freemium, coaching, white-label) without selling user data

---

## Features

| Area | What you get |
|------|----------------|
| **Auth** | Username + bcrypt-hashed password. No shared accounts. |
| **Dashboard** | Today’s workouts, calories, protein, plan overview, macro targets |
| **Profile** | Age, sex, height, weight, activity, goal → BMR / TDEE / macros; body-weight log; 1RM estimator |
| **Programs** | 50+ ready-made templates (beginner → advanced, home, rehab, olympic, etc.) |
| **Builder** | Build or edit plans, set sets/reps/rest/weight, log a session in one click |
| **Library** | 200+ exercises with YouTube form search links |
| **Nutrition** | Log foods (per 100 g database), daily totals |
| **Progress** | Volume and body-weight charts (Plotly) |
| **Journal** | Free-text training reflections |
| **Recovery** | Practical nutrition / recovery / progression tips |
| **Share / QR** | Generate a QR code for your live app URL and download the PNG |
| **Theme** | Light UI by default with a Dark mode toggle in the sidebar |
| **Security & Data** | Export / import JSON backup; clear privacy notes |

Data is stored in a local **SQLite** database under `data/wos4e.db`, keyed by `user_id`. Other users cannot read your rows.

---

## Quick start (local)

```bash
git clone <your-repo-url>
cd wos4e-streamlit
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501).  
Create an account → set Profile → load a Program → log workouts.

---

## Deploy to Streamlit Community Cloud

1. Push this folder to a **public or private** GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Select the repo, branch, and main file `app.py`.
4. Deploy.

### Important: persistence on Community Cloud

The free Community Cloud filesystem is **ephemeral**. The SQLite file can be wiped on reboot.

**Recommended options:**

- Use **Export my data** regularly and re-import after a reset, **or**
- Attach an external database (Supabase, Neon, PlanetScale, etc.) and replace `utils/db.py` — the rest of the app stays the same, **or**
- Self-host on a VPS / Railway / Render with a persistent volume.

Optional secret (Settings → Secrets):

```toml
APP_URL = "https://your-app-name.streamlit.app"
```

This pre-fills the QR code page.

---

## Security notes

- Passwords: **bcrypt** with unique salt.
- Session: Streamlit session state only; no cookies with credentials.
- Isolation: every query is scoped by `user_id`.
- No third-party analytics or data brokers in this codebase.
- Not a medical device — general fitness guidance only.

---

## Ownership & monetization

This repository is an **original implementation**. You control the license (add an `LICENSE` file of your choice — MIT, proprietary, etc.).

Ideas that respect privacy:

1. Freemium (unlock advanced programs / analytics).
2. Sell self-hosted licenses to coaches and gyms.
3. Affiliate links with clear disclosure.
4. Optional paid coaching layered on top of the journal + progress tools.
5. White-label deployments.

Do **not** sell or share individual user training data.

---

## Project layout

```
wos4e-streamlit/
├── app.py              # Main Streamlit entrypoint
├── requirements.txt
├── README.md
├── utils/
│   ├── auth.py         # Password hashing
│   ├── calc.py         # BMR, TDEE, macros, 1RM, volume
│   ├── data.py         # Exercise library, programs, foods
│   └── db.py           # SQLite user + data isolation
├── data/               # Created at runtime (gitignored)
└── assets/             # Optional images
```

---

## License

Add your preferred license. Suggested starting point for open sharing: MIT.  
For commercial exclusivity, use a proprietary license and keep the repo private.
