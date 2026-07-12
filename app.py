import streamlit as st
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
# 🔐 LOAD API
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# 🎨 PAGE SETTINGS
st.set_page_config(page_title="AI Marketing Pro", layout="wide")

# 🎨 CUSTOM UI DESIGN
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #262730;
        color: white;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# 🔐 LOGIN STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🔐 LOGIN FUNCTION
def login():
    st.markdown("## 🔐 Welcome Back")
    st.markdown("Login to access your AI Marketing Dashboard")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        user = st.text_input("👤 Username")
        pwd = st.text_input("🔑 Password", type="password")

        if st.button("🚀 Login"):
            if user == "admin" and pwd == "1234":
                st.session_state.logged_in = True
                st.success("✅ Login Successful!")
            else:
                st.error("❌ Invalid login")

# 🚫 STOP IF NOT LOGGED IN
if not st.session_state.logged_in:
    login()
    st.stop()

# 🚀 HEADER
st.markdown("""
# 🚀 AI Marketing Pro Dashboard
### 💼 Smart Tools for Digital Growth
""")
st.divider()

# 📌 TABS
tab1, tab2, tab3, tab4 = st.tabs([
    "📸 Instagram AI",
    "🤖 Chatbot",
    "📋 Leads",
    "📊 History"
])

# 📸 INSTAGRAM AI
with tab1:
    st.subheader("📸 Instagram AI Generator")

    topic = st.text_input("💡 Enter your product/topic")

    if st.button("✨ Generate Marketing Content"):
        if topic:
            st.info("⏳ Generating content...")

            prompt = f"""
            Create:
            - Instagram caption with emojis
            - 15 trending hashtags
            - 3 reel ideas
            - Caption in English and Kannada
            Topic: {topic}
            """

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            output = res.choices[0].message.content

            st.success("✅ Content Ready!")
            st.markdown(output)

            with open("content.txt", "a") as f:
                f.write(f"\n--- {datetime.now()} ---\n{output}\n")

        else:
            st.warning("⚠️ Please enter a topic")

# 🤖 CHATBOT
with tab2:
    st.subheader("🤖 AI Chatbot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask something")

    if st.button("Send"):
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})

            res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.chat_history
            )

            reply = res.choices[0].message.content
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"**👤 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 AI:** {msg['content']}")

# 📋 LEADS
with tab3:
    st.subheader("📋 Lead Collection")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    if st.button("Save Lead"):
        if name and email:
            df = pd.DataFrame([{
                "Name": name,
                "Email": email,
                "Phone": phone,
                "Time": datetime.now()
            }])

            try:
                df.to_csv("leads.csv", mode='a', header=False, index=False)
            except:
                df.to_csv("leads.csv", index=False)

            st.success("✅ Saved!")

    if os.path.exists("leads.csv"):
        with open("leads.csv", "r") as f:
            st.download_button("⬇️ Download Leads", f, "leads.csv")

# 📊 HISTORY
with tab4:
    st.subheader("📊 Content History")

    try:
        with open("content.txt", "r") as f:
            st.text(f.read())
    except:
        st.warning("No history yet")