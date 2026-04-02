import streamlit as st
import base64
from ai_engine import generate_roadmap, generate_explanation, generate_resources, chatbot_response
from auth import signup_user, login_user, save_history, get_history

st.set_page_config(page_title="Learnova", page_icon="🚀", layout="centered")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "selected_query" not in st.session_state:
    st.session_state.selected_query = None

if "selected_response" not in st.session_state:
    st.session_state.selected_response = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

# ---------------- GLOBAL CSS FIX ----------------
st.markdown("""
<style>

/* Input box */
div[data-testid="stTextInput"] input {
    border-radius: 10px;
    padding: 10px;
}

/* Placeholder */
div[data-testid="stTextInput"] input::placeholder {
    color: gray !important;
}

/* Button */
div.stButton > button {
    background-color: #333;
    color: white;
    border-radius: 10px;
}
div.stButton > button:hover {
    background-color: #555;
}

/* ONLY content text (safe, no heading override) */
.custom-text p, .custom-text li {
    color: #222 !important;
    font-size: 16px;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# ---------------- BACKGROUND ----------------
def set_bg():
    with open("background-animation-gif-download-7501790.mp4", "rb") as video_file:
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode()

    st.markdown(f"""
    <style>
        div[data-testid="stTextInput"] label {{
            color: #a14838 !important;
            font-size: 20px !important;
            font-weight: bold;
        }}

        div[data-testid="stTextInput"] input {{
            color: #9c9835 !important;
        }}

        div[data-testid="stTextInput"] input::placeholder {{
            color: #42f5da !important;
        }}

        .stApp {{
            background: none;
        }}

        video {{
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            object-fit: cover;
            z-index: -2;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255,255,255,0.6);
            z-index: -1;
        }}

        .title {{
            text-align: center;
            font-size: 60px;
            font-weight: 700;
            color: #eb2525;
        }}

        .subtitle {{
            text-align: center;
            font-size: 30px;
            font-weight: 400;
            color: #448727;
            margin-bottom: 30px;
        }}
    </style>

    <video autoplay loop muted>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
menu = ["Login", "Signup"]
choice = st.sidebar.selectbox("Menu", menu)

set_bg()
# ---------------- LOGIN SYSTEM ----------------
if not st.session_state.logged_in:

    if choice == "Login":
        st.markdown('<div class="title">🔐 Login</div>', unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            result = login_user(username, password)

            if result:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

    elif choice == "Signup":
        st.markdown('<div class="title">📝 Signup</div>', unsafe_allow_html=True)

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Create Account"):
            success = signup_user(new_user, new_pass)

            if success:
                st.success("Account created ✅ Now login")
            else:
                st.error("Username already exists ❌")


# ---------------- MAIN APP ----------------
else:

    st.sidebar.success(f"Welcome {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # -------- HISTORY --------
    st.sidebar.markdown("### 🕓 History")

    history = get_history(st.session_state.username)

    for i,(q, r) in enumerate(history[::-1]):
        if st.sidebar.button(q,key=f"history_{i}"):
            st.session_state.selected_query = q
            st.session_state.selected_response = r
            st.session_state.chat_history=[]

    # -------- UI --------
    st.markdown('<div class="title">🚀 Learnova</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your AI-powered personalized learning mentor</div>', 
                unsafe_allow_html=True)

    st.markdown('<h3 style="color:#a14838;">📚 Enter Topic</h3>', unsafe_allow_html=True)
    topic = st.text_input("", placeholder="Reply to Learnova")

    if st.button("✨ Generate Roadmap"):
        if topic:
            st.session_state.chat_history=[]
            st.session_state.chat_input=""
            st.session_state.selected_query=None
            st.session_state.selected_response=None
            with st.spinner("Generating with AI... ⏳"):

                roadmap = generate_roadmap(topic)
                st.markdown("<h3 style='color:#00c4cc;'>🗺 Learning Roadmap</h3>",unsafe_allow_html=True)
                st.markdown(f"""<div style='color:#131414; font-size:16px; line-height:1.6;'>{roadmap}</div>
                             """, unsafe_allow_html=True)

                # Explanation
                explanation=generate_explanation(topic)
                st.markdown("<h3 style='color:#ff9800;'>📘 Explanation</h3>",unsafe_allow_html=True)
                st.markdown(f"""<div style='color:#131414; font-size:16px; line-height:1.6;'>{explanation}</div>
                             """, unsafe_allow_html=True)

                # Resources
                resources=generate_resources(topic)
                st.markdown("<h3 style='color:#4caf50;'>🔗 Resources</h3>",unsafe_allow_html=True)
                st.markdown(f"""<div style='color:black; font-size:16px; line-height:1.6;'>{resources}</div>
                             """, unsafe_allow_html=True)

                # ✅ SAVE HISTORY
                full_response = f"{roadmap}\n\n{explanation}\n\n{resources}"
                save_history(st.session_state.username, topic, full_response)

        else:
            st.markdown("""<div style='
                    background-color:#ffe6e6;
                    color:#9e912b;
                    padding:15px;
                    border-radius:10px;
                    border-left:6px solid red;
                    font-weight:bold;
                    '>⚠️ Please enter a topic first.</div>""", unsafe_allow_html=True)

    # -------- SHOW PREVIOUS --------
    if st.session_state.selected_query:
        st.markdown("<h2 style='color:black;'>📌 Previous Search</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='color:black; font-size:18px; font-weight:bold;'>{st.session_state.selected_query}</div>", 
                    unsafe_allow_html=True)

        st.markdown(f"<div style='color:#222; font-size:16px; line-height:1.6;'>{st.session_state.selected_response}</div>", 
                    unsafe_allow_html=True)

    # -------- CHATBOT --------
    st.divider()
    st.markdown("<h2 style='color:#985099;'>🤖 Ask Learnova</h2>",unsafe_allow_html=True)

    q = st.text_input("Ask anything...",key="chat_input")

    if q:
        response = chatbot_response(q)
        st.info(response)

        
