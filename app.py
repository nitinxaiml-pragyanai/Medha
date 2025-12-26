import streamlit as st
import wikipedia
from groq import Groq
import time

# ==========================================
# 1. LEGENDARY GUI CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="MEDHA AI",
    page_icon="🧠",
    layout="centered"
)

# 🎨 THE LEGENDARY THEME (Cyber-Glass CSS)
st.markdown("""
<style>
    /* 1. IMPORT FUTURISTIC FONT */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500&display=swap');

    /* 2. BACKGROUND: Deep Space Cyberpunk */
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(circle at 50% 50%, #1a1a2e 0%, #000000 100%);
        color: #e0e0e0;
    }

    /* 3. HEADERS: Neon Glow */
    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #00e5ff !important;
        text-shadow: 0 0 10px #00e5ff, 0 0 20px #00e5ff;
        text-align: center;
        letter-spacing: 2px;
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    
    h3 {
        font-family: 'Orbitron', sans-serif;
        color: #ff007f !important;
        border-bottom: 2px solid #ff007f;
        padding-bottom: 10px;
    }

    /* 4. GLASSMORPHISM CARDS */
    .stTextInput > div > div > input {
        background-color: rgba(20, 20, 20, 0.8) !important;
        color: #00e5ff !important;
        border: 1px solid #00e5ff !important;
        border-radius: 10px;
        font-family: 'Rajdhani', sans-serif;
        font-size: 18px;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
        border-color: #ffffff !important;
    }

    div[data-testid="stStatusWidget"] {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid #333;
        color: #00ff00;
    }

    /* 5. STREAMING TEXT STYLE */
    .element-container {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.1rem;
    }

    /* 6. ANIMATIONS */
    @keyframes glow {
        from { text-shadow: 0 0 10px #00e5ff; }
        to { text-shadow: 0 0 20px #00e5ff, 0 0 30px #00e5ff; }
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LOGIC CORE (Groq + Wikipedia)
# ==========================================

# Sidebar for Key
with st.sidebar:
    st.markdown("### 🔐 ACCESS MEDHA")
    api_key = st.text_input("Groq API Key", type="password")
    st.markdown("[Get Key Here](https://console.groq.com/keys)")
    st.markdown("---")
    st.markdown("Running on **LPU Speed Engine**")

# Main Interface
st.title("MEDHA AI")
st.markdown("<div style='text-align: center; font-family: Rajdhani; color: #888;'>THE OMNISCIENT INTERFACE</div>", unsafe_allow_html=True)
st.markdown("---")

# The Query Box
query = st.text_input("", placeholder="Ask the Hive Mind... (e.g. Quantum Physics)")

# Execution Logic
if query and api_key:
    # A. Visual Feedback
    with st.status("🚀 INITIATING NEURAL LINK...", expanded=True) as status:
        try:
            # 1. Retrieve Data
            st.write("📡 Scanning Global Knowledge Base...")
            wiki_page = wikipedia.page(query, auto_suggest=True)
            raw_text = wiki_page.content[:5000] # Feed 5k chars
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
                    {"role": "system", "content": "You are MEDHA, a futuristic AI. Summarize the text in deep detail but using bullet points. Use a professional, scientific tone. Do not say 'Here is a summary'."},
                    {"role": "user", "content": raw_text}
                ],
                temperature=0.5,
                max_tokens=500,
                stream=True
            )

            # D. Render Character by Character
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # Add a blinking cursor effect
                    response_container.markdown(full_response + " █")
            
            # Final Clean Render
            response_container.markdown(full_response)

        except wikipedia.exceptions.DisambiguationError as e:
            st.error(f"⚠️ AMBIGUOUS SIGNAL. DID YOU MEAN: {', '.join(e.options[:3])}")
        except wikipedia.exceptions.PageError:
            st.error("❌ SIGNAL LOST. TOPIC NOT FOUND.")
        except Exception as e:
            st.error(f"❌ SYSTEM FAILURE: {str(e)}")

elif query and not api_key:
    st.warning("⚠️ SECURITY ALERT: API KEY REQUIRED")

