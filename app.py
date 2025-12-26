import streamlit as st
import wikipedia
from groq import Groq
import time

# ==========================================
# 1. CONFIGURATION & SECRETS
# ==========================================
st.set_page_config(
    page_title="MEDHA AI",
    page_icon="🧠",
    layout="centered"
)

# Load Key securely
try:
    api_key = st.secrets["GROQ_API_KEY"]
except FileNotFoundError:
    st.error("❌ CRITICAL ERROR: Secrets file not found. Please set up .streamlit/secrets.toml")
    st.stop()
except KeyError:
    st.error("❌ CRITICAL ERROR: 'GROQ_API_KEY' not found in secrets.")
    st.stop()

# ==========================================
# 2. THE "ROYAL BLUE" LEGENDARY THEME
# ==========================================
st.markdown("""
<style>
    /* 1. FORCE WHITE TEXT */
    .stApp, p, h1, h2, h3, label, .stMarkdown, .stWrite {
        color: #ffffff !important;
    }

    /* 2. BACKGROUND: ROYAL IMPERIAL BLUE GRADIENT */
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #003366 50%, #00509e 100%);
        background-attachment: fixed;
    }

    /* 3. LIQUID GLASS INPUT (Blue Tint) */
    .stTextInput > div > div > input {
        background: rgba(0, 80, 158, 0.2) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    }
    
    .stTextInput > div > div > input:focus {
        border: 1px solid #4da6ff !important;
        box-shadow: 0 0 20px rgba(77, 166, 255, 0.4);
        background: rgba(0, 80, 158, 0.4) !important;
    }

    /* 4. LIQUID GLASS BUTTONS */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background: rgba(77, 166, 255, 0.3); /* Royal Blue Glow */
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(77, 166, 255, 0.5);
        border-color: #4da6ff;
    }
    
    /* 5. HEADER GLOW */
    h1 {
        text-shadow: 0 0 10px #4da6ff, 0 0 20px #003366;
    }

    /* REMOVE JUNK */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. THE INTERFACE
# ==========================================

st.title("MEDHA AI")
st.markdown("<div style='text-align: center; color: #aaccff; margin-bottom: 20px; font-weight: 300;'>THE ROYAL INTERFACE</div>", unsafe_allow_html=True)

# The Search Box
query = st.text_input("", placeholder="Ask Medha... (e.g. History of India)")

# Execution Logic
if query:
    # A. Visual Feedback
    with st.status("🚀 INITIATING NEURAL LINK...", expanded=True) as status:
        try:
            # 1. Retrieve Data
            st.write("📡 Scanning Global Knowledge Base...")
            wiki_page = wikipedia.page(query, auto_suggest=True)
            raw_text = wiki_page.content[:6000] # Increased context
            st.write(f"✅ Target Locked: {wiki_page.title}")
            
            # 2. Activate Groq
            st.write("⚡ Engaging LPU Engine (Llama 3.1)...")
            client = Groq(api_key=api_key)
            
            status.update(label="INTELLIGENCE ACQUIRED", state="complete", expanded=False)

            # B. The Display
            st.markdown(f"### ⚡ ANALYSIS: {wiki_page.title.upper()}")
            
            # Streaming Container
            response_container = st.empty()
            full_response = ""
            
            # C. The Stream (UPDATED MODEL ID HERE)
            stream = client.chat.completions.create(
                model="llama-3.1-8b-instant",  # <--- FIXED MODEL ID
                messages=[
                    {"role": "system", "content": "You are MEDHA, a sophisticated AI. Summarize the provided text in 5-7 clear, professional bullet points. Be concise but deep. Do not use conversational filler."},
                    {"role": "user", "content": raw_text}
                ],
                temperature=0.5,
                max_tokens=600,
                stream=True
            )

            # D. Render
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    response_container.markdown(full_response + " █")
            
            response_container.markdown(full_response)

        except wikipedia.exceptions.DisambiguationError as e:
            st.error(f"⚠️ AMBIGUOUS SIGNAL. DID YOU MEAN: {', '.join(e.options[:3])}")
        except wikipedia.exceptions.PageError:
            st.error("❌ SIGNAL LOST. TOPIC NOT FOUND.")
        except Exception as e:
            st.error(f"❌ SYSTEM FAILURE: {str(e)}")
