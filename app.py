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

# Load Key securely from secrets.toml (or Cloud Secrets)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except FileNotFoundError:
    st.error("❌ CRITICAL ERROR: Secrets file not found. Please set up .streamlit/secrets.toml")
    st.stop()
except KeyError:
    st.error("❌ CRITICAL ERROR: 'GROQ_API_KEY' not found in secrets.")
    st.stop()

# ==========================================
# 2. THE "LIQUID GLASS" THEME (Apple Style)
# ==========================================
st.markdown("""
<style>
    /* 1. GLOBAL TEXT FIX */
    .stApp, p, h1, h2, h3, label, .stMarkdown {
        color: #ffffff !important; /* Force white text everywhere */
    }

    /* 2. BACKGROUND: Deep Space Gradient */
    .stApp {
        background: radial-gradient(circle at center, #1e1e2f 0%, #000000 100%);
    }

    /* 3. LIQUID GLASS INPUT BOX */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important; /* Mostly transparent */
        backdrop-filter: blur(10px); /* The Frost Effect */
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #00e5ff !important;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border: 1px solid #00e5ff !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
        background: rgba(255, 255, 255, 0.1) !important;
    }

    /* 4. LIQUID GLASS BUTTONS (The Apple Look) */
    div.stButton > button {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        background: rgba(0, 229, 255, 0.2); /* Neon cyan tint on hover */
        border: 1px solid rgba(0, 229, 255, 0.5);
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 229, 255, 0.4);
    }

    /* 5. REMOVE DEFAULT JUNK */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. THE INTERFACE
# ==========================================

st.title("MEDHA AI")
st.markdown("<div style='text-align: center; color: #888; margin-bottom: 20px;'>THE GLASS INTERFACE</div>", unsafe_allow_html=True)

# The Search Box
query = st.text_input("", placeholder="Ask the Hive Mind... (e.g. Black Holes)")

# Execution Logic
if query:
    # A. Visual Feedback
    with st.status("🚀 INITIATING NEURAL LINK...", expanded=True) as status:
        try:
            # 1. Retrieve Data
            st.write("📡 Scanning Global Knowledge Base...")
            wiki_page = wikipedia.page(query, auto_suggest=True)
            raw_text = wiki_page.content[:5000]
            st.write(f"✅ Target Locked: {wiki_page.title}")
            
            # 2. Activate Groq
            st.write("⚡ Engaging LPU Inference Engine...")
            client = Groq(api_key=api_key)
            
            status.update(label="INTELLIGENCE ACQUIRED", state="complete", expanded=False)

            # B. The Display
            st.markdown(f"### ⚡ ANALYSIS: {wiki_page.title.upper()}")
            
            # Streaming Container
            response_container = st.empty()
            full_response = ""
            
            # C. The Stream
            stream = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are MEDHA, a futuristic AI. Summarize the text in deep detail but using bullet points. Use a professional, scientific tone."},
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
