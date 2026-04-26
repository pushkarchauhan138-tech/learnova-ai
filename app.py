import streamlit as st
import base64
from ai_engine import generate_roadmap, generate_explanation, generate_resources, chatbot_response
from auth import signup_user, login_user, save_history, get_history

st.set_page_config(page_title="Learnova", page_icon="⚡", layout="centered")

# ---------------- SESSION STATE ----------------
defaults = {
    "logged_in": False,
    "username": "",
    "selected_query": None,
    "selected_response": None,
    "chat_history": [],
    "page": "login",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* ---- PAGE BACKGROUND ---- */
.stApp {
    background: #0a0a0f !important;
    color: #f0eeff !important;
}

/* Hide default streamlit header/footer */
#MainMenu, footer, header { visibility: hidden; }

/* ---- ANIMATED GRADIENT BG ---- */
.stApp::before {
    content: '';
    position: fixed;
    top: -200px; left: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(124,92,252,0.15) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: orb1 8s ease-in-out infinite alternate;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -200px; right: -200px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(0,212,170,0.10) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
    animation: orb2 10s ease-in-out infinite alternate-reverse;
}
@keyframes orb1 { 0% { transform: translate(0,0); } 100% { transform: translate(60px,40px); } }
@keyframes orb2 { 0% { transform: translate(0,0); } 100% { transform: translate(-50px,30px); } }

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 0.5px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] * { color: #b0aac8 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 0.5px solid rgba(255,255,255,0.1) !important;
    color: #b0aac8 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.2s !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(124,92,252,0.12) !important;
    border-color: #7c5cfc !important;
    color: #a98bff !important;
}

/* ---- TEXT INPUTS ---- */
div[data-testid="stTextInput"] input {
    background: #111118 !important;
    border: 0.5px solid rgba(255,255,255,0.15) !important;
    border-radius: 14px !important;
    color: #f0eeff !important;
    padding: 14px 18px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 16px !important;
    transition: border-color 0.3s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #7c5cfc !important;
    box-shadow: 0 0 0 3px rgba(124,92,252,0.15) !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #6b6585 !important; }
div[data-testid="stTextInput"] label {
    color: #8884a0 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

/* ---- BUTTONS ---- */
div.stButton > button {
    background: linear-gradient(135deg, #7c5cfc, #5a3dd4) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,92,252,0.4) !important;
}
div.stButton > button:active { transform: scale(0.97) !important; }

/* ---- SPINNER ---- */
.stSpinner > div { border-top-color: #7c5cfc !important; }

/* ---- ALERTS ---- */
.stSuccess {
    background: rgba(0,212,170,0.12) !important;
    border: 0.5px solid rgba(0,212,170,0.3) !important;
    border-radius: 12px !important;
    color: #00d4aa !important;
}
.stError {
    background: rgba(255,107,107,0.12) !important;
    border: 0.5px solid rgba(255,107,107,0.3) !important;
    border-radius: 12px !important;
    color: #ff6b6b !important;
}
.stInfo {
    background: rgba(124,92,252,0.10) !important;
    border: 0.5px solid rgba(124,92,252,0.25) !important;
    border-radius: 12px !important;
    color: #a98bff !important;
}

/* ---- DIVIDER ---- */
hr { border-color: rgba(255,255,255,0.08) !important; }

/* ---- SELECTBOX ---- */
div[data-testid="stSelectbox"] > div > div {
    background: #111118 !important;
    border: 0.5px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
    color: #f0eeff !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- COMPONENTS ----------------

def hero_banner(title: str, subtitle: str, tag: str = None):
    tag_html = f"""
    <div style="display:inline-flex;align-items:center;gap:8px;padding:6px 14px;
        border-radius:999px;border:0.5px solid rgba(124,92,252,0.3);
        background:rgba(124,92,252,0.08);font-size:12px;color:#a98bff;
        margin-bottom:18px;letter-spacing:.5px;text-transform:uppercase;">
        <span style="width:6px;height:6px;border-radius:50%;background:#7c5cfc;
            display:inline-block;animation:pulse 2s ease infinite;"></span>
        {tag}
    </div>
    """ if tag else ""

    st.markdown(f"""
    <style>
    @keyframes pulse {{
        0%,100%{{opacity:1;box-shadow:0 0 0 0 rgba(124,92,252,0.5)}}
        50%{{opacity:.7;box-shadow:0 0 0 8px transparent}}
    }}
    @keyframes fadeUp {{
        from{{opacity:0;transform:translateY(20px)}}
        to{{opacity:1;transform:translateY(0)}}
    }}
    </style>
    <div style="text-align:center;padding:40px 0 10px;animation:fadeUp .6s ease;">
        {tag_html}
        <h1 style="font-family:'Syne',sans-serif;font-size:clamp(36px,5vw,60px);
            font-weight:800;letter-spacing:-2px;line-height:1.1;margin-bottom:14px;
            background:linear-gradient(135deg,#f0eeff 0%,#a98bff 50%,#00d4aa 100%);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
            {title}
        </h1>
        <p style="font-size:17px;color:#8884a0;max-width:480px;margin:0 auto;line-height:1.7;">
            {subtitle}
        </p>
    </div>
    """, unsafe_allow_html=True)


def result_card(icon: str, title: str, content: str, accent: str = "#7c5cfc"):
    st.markdown(f"""
    <div style="background:#111118;border:0.5px solid rgba(255,255,255,0.08);
        border-radius:16px;padding:28px;margin-bottom:16px;position:relative;overflow:hidden;
        animation:fadeUp .5s ease;">
        <div style="position:absolute;top:0;left:0;right:0;height:2px;
            background:linear-gradient(90deg,transparent,{accent},transparent);"></div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
            <div style="width:36px;height:36px;border-radius:10px;display:flex;
                align-items:center;justify-content:center;font-size:18px;
                background:#18181f;">{icon}</div>
            <div style="font-family:'Syne',sans-serif;font-size:16px;font-weight:700;
                color:#f0eeff;">{title}</div>
        </div>
        <div style="color:#b8b4d0;font-size:15px;line-height:1.75;">{content}</div>
    </div>
    """, unsafe_allow_html=True)


def stat_row():
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:28px 0;">
        <div style="background:#111118;border:0.5px solid rgba(255,255,255,0.08);
            border-radius:14px;padding:20px;text-align:center;">
            <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;
                background:linear-gradient(135deg,#7c5cfc,#00d4aa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">500+</div>
            <div style="font-size:12px;color:#6b6585;margin-top:4px;
                text-transform:uppercase;letter-spacing:.5px;">Topics</div>
        </div>
        <div style="background:#111118;border:0.5px solid rgba(255,255,255,0.08);
            border-radius:14px;padding:20px;text-align:center;">
            <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;
                background:linear-gradient(135deg,#7c5cfc,#00d4aa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">10K+</div>
            <div style="font-size:12px;color:#6b6585;margin-top:4px;
                text-transform:uppercase;letter-spacing:.5px;">Learners</div>
        </div>
        <div style="background:#111118;border:0.5px solid rgba(255,255,255,0.08);
            border-radius:14px;padding:20px;text-align:center;">
            <div style="font-family:'Syne',sans-serif;font-size:28px;font-weight:800;
                background:linear-gradient(135deg,#7c5cfc,#00d4aa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">∞</div>
            <div style="font-size:12px;color:#6b6585;margin-top:4px;
                text-transform:uppercase;letter-spacing:.5px;">Possibilities</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def section_header(text: str, color: str = "#a98bff"):
    st.markdown(f"""
    <h3 style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
        color:{color};margin:24px 0 12px;display:flex;align-items:center;gap:8px;">
        {text}
    </h3>
    """, unsafe_allow_html=True)


# ---------------- AUTH PAGES ----------------

def page_login():
    hero_banner(
        "Welcome Back ⚡",
        "Sign in to continue your personalized learning journey.",
        "AI-Powered Learning"
    )
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background:#111118;border:0.5px solid rgba(255,255,255,0.08);
            border-radius:20px;padding:36px 32px;margin-top:10px;">
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter your username", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("🔐 Sign In", use_container_width=True):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

        st.markdown("""</div>""", unsafe_allow_html=True)


def page_signup():
    hero_banner(
        "Join Learnova 🚀",
        "Create your account and start learning with AI today.",
        "Get Started Free"
    )
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background:#111118;border:0.5px solid rgba(255,255,255,0.08);
            border-radius:20px;padding:36px 32px;margin-top:10px;">
        """, unsafe_allow_html=True)

        new_user = st.text_input("Choose Username", placeholder="Pick a cool username", key="signup_user")
        new_pass = st.text_input("Create Password", type="password", placeholder="Strong password", key="signup_pass")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("✨ Create Account", use_container_width=True):
            if signup_user(new_user, new_pass):
                st.success("Account created ✅ Now login!")
            else:
                st.error("Username already exists ❌")

        st.markdown("""</div>""", unsafe_allow_html=True)


# ---------------- MAIN APP ----------------

def page_main():
    # ---- SIDEBAR ----
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:16px 0 8px;">
            <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:800;
                background:linear-gradient(135deg,#7c5cfc,#00d4aa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;margin-bottom:4px;">⚡ Learnova</div>
            <div style="font-size:13px;color:#6b6585;">
                Welcome back, <span style="color:#a98bff;">{st.session_state.username}</span>
            </div>
        </div>
        <hr style="border-color:rgba(255,255,255,0.07);margin:12px 0;">
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.chat_history = []
            st.rerun()

        st.markdown("""
        <div style="margin-top:20px;font-size:12px;color:#6b6585;
            text-transform:uppercase;letter-spacing:.7px;font-weight:600;margin-bottom:10px;">
            📂 History
        </div>
        """, unsafe_allow_html=True)

        history = get_history(st.session_state.username)
        for i, (q, r) in enumerate(history[::-1][:8]):
            if st.button(f"🔖 {q[:28]}{'...' if len(q)>28 else ''}", key=f"hist_{i}"):
                st.session_state.selected_query = q
                st.session_state.selected_response = r
                st.session_state.chat_history = []

    # ---- HERO ----
    hero_banner(
        "Learn Anything.<br>Master Everything.",
        "Enter any topic and get a personalized roadmap, deep explanation, and curated resources — instantly.",
        "AI-Powered Learning Mentor"
    )
    stat_row()

    # ---- TOPIC INPUT ----
    section_header("📚 Enter Topic")

    col_input, col_btn = st.columns([4, 1])
    with col_input:
        topic = st.text_input(
            "",
            placeholder="e.g. Machine Learning, React, Quantum Physics...",
            key="topic_input",
            label_visibility="collapsed"
        )
    with col_btn:
        st.markdown("<div style='height:5px'></div>", unsafe_allow_html=True)
        generate_clicked = st.button("✨ Generate", use_container_width=True)

    # Quick chips
    st.markdown("""
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 28px;">
        <span style="padding:6px 14px;border-radius:999px;border:0.5px solid rgba(255,255,255,0.1);
            font-size:12px;color:#8884a0;background:#111118;cursor:pointer;">
            Machine Learning</span>
        <span style="padding:6px 14px;border-radius:999px;border:0.5px solid rgba(255,255,255,0.1);
            font-size:12px;color:#8884a0;background:#111118;">Web Development</span>
        <span style="padding:6px 14px;border-radius:999px;border:0.5px solid rgba(255,255,255,0.1);
            font-size:12px;color:#8884a0;background:#111118;">Data Science</span>
        <span style="padding:6px 14px;border-radius:999px;border:0.5px solid rgba(255,255,255,0.1);
            font-size:12px;color:#8884a0;background:#111118;">Python</span>
        <span style="padding:6px 14px;border-radius:999px;border:0.5px solid rgba(255,255,255,0.1);
            font-size:12px;color:#8884a0;background:#111118;">System Design</span>
    </div>
    """, unsafe_allow_html=True)

    # ---- GENERATE ----
    if generate_clicked:
        if not topic:
            st.markdown("""
            <div style="background:rgba(255,107,107,0.1);color:#ff9090;
                padding:14px 18px;border-radius:12px;border-left:3px solid #ff6b6b;
                font-weight:500;margin-bottom:16px;">
                ⚠️ Please enter a topic first.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.session_state.chat_history = []
            st.session_state.selected_query = None
            st.session_state.selected_response = None

            with st.spinner("🤖 Generating your personalized learning plan..."):
                roadmap = generate_roadmap(topic)
                explanation = generate_explanation(topic)
                resources = generate_resources(topic)

            result_card("🗺️", "Learning Roadmap", roadmap, "#7c5cfc")
            result_card("📘", "Explanation", explanation, "#00d4aa")
            result_card("🔗", "Resources", resources, "#ff6b6b")

            full_response = f"{roadmap}\n\n{explanation}\n\n{resources}"
            save_history(st.session_state.username, topic, full_response)

    # ---- PREVIOUS SEARCH ----
    if st.session_state.selected_query:
        st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:32px 0;'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="margin-bottom:16px;">
            <div style="font-size:12px;color:#6b6585;text-transform:uppercase;
                letter-spacing:.7px;margin-bottom:6px;">📌 Previous Search</div>
            <div style="font-family:'Syne',sans-serif;font-size:20px;font-weight:700;
                color:#f0eeff;">{st.session_state.selected_query}</div>
        </div>
        """, unsafe_allow_html=True)
        result_card("📋", "Saved Response", st.session_state.selected_response, "#7c5cfc")

    # ---- CHATBOT ----
    st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin:36px 0 24px;'>", unsafe_allow_html=True)
    section_header("🤖 Ask Learnova", "#c084fc")

    # Render chat history
    for msg in st.session_state.chat_history:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:10px;">
                <div style="background:rgba(124,92,252,0.15);border:0.5px solid rgba(124,92,252,0.3);
                    border-radius:14px 14px 4px 14px;padding:12px 16px;max-width:80%;
                    color:#f0eeff;font-size:15px;line-height:1.6;">{content}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:10px;">
                <div style="background:#111118;border:0.5px solid rgba(255,255,255,0.08);
                    border-radius:14px 14px 14px 4px;padding:12px 16px;max-width:80%;
                    color:#b8b4d0;font-size:15px;line-height:1.65;">{content}</div>
            </div>
            """, unsafe_allow_html=True)

    chat_q = st.text_input(
        "",
        placeholder="Ask anything about the topic...",
        key="chat_input_box",
        label_visibility="collapsed"
    )

    if chat_q:
        st.session_state.chat_history.append({"role": "user", "content": chat_q})
        with st.spinner("Thinking..."):
            response = chatbot_response(chat_q)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()


# ---------------- ROUTER ----------------
if not st.session_state.logged_in:
    menu_choice = st.sidebar.selectbox("", ["Login", "Signup"], label_visibility="collapsed")
    st.sidebar.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;
        background:linear-gradient(135deg,#7c5cfc,#00d4aa);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;padding:16px 0 4px;text-align:center;">⚡ Learnova</div>
    """, unsafe_allow_html=True)

    if menu_choice == "Login":
        page_login()
    else:
        page_signup()
else:
    page_main()
