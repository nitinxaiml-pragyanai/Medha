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
    st.error("❌ CRITICAL ERROR: Secrets file not found.")
    st.stop()
except KeyError:
    st.error("❌ CRITICAL ERROR: 'GROQ_API_KEY' not found in secrets.")
    st.stop()

# ==========================================
# 2. THE ROYAL BLUE THEME (CSS)
# ==========================================
st.markdown("""
<style>
    /* FORCE WHITE TEXT */
    .stApp, p, h1, h2, h3, label, .stMarkdown, .stWrite, .stRadio {
        color: #ffffff !important;
    }

    /* ROYAL BLUE GRADIENT BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #003366 50%, #00509e 100%);
        background-attachment: fixed;
    }

    /* GLASS INPUT BOX */
    .stTextInput > div > div > input {
        background: rgba(0, 80, 158, 0.2) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        border-radius: 12px;
        padding: 12px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4da6ff !important;
        box-shadow: 0 0 15px rgba(77, 166, 255, 0.5);
    }

    /* TABS STYLE */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4da6ff !important;
        color: white !important;
    }

    /* DOWNLOAD BUTTON STYLE */
    div.stDownloadButton > button {
        background: linear-gradient(45deg, #ff007f, #ff4081);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        transition: transform 0.2s;
    }
    div.stDownloadButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 10px #ff007f;
    }

    /* HIDE JUNK */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. THE INTERFACE
# ==========================================

st.title("MEDHA AI")
st.markdown("<div style='text-align: center; color: #aaccff; margin-bottom: 20px; font-weight: 300;'>A PRODUCT OF SAMRION Ltd.</div>", unsafe_allow_html=True)

# The Search Box
query = st.text_input("", placeholder="Ask Medha... (e.g. History of India)")

# Execution Logic
if query:
    # 1. DATA FETCHING (Outside the tabs to save state)
    try:
        # Use a spinner instead of a collapsible status box
        with st.spinner("📡 Scanning Global Knowledge Base..."):
            wiki_page = wikipedia.page(query, auto_suggest=True)
            raw_text = wiki_page.content
            title = wiki_page.title
            
            # Smart truncation for AI (first 6000 chars)
            ai_input_text = raw_text[:6000]

        # 2. SUCCESS HEADER
        st.success(f"✅ TARGET LOCKED: {title.upper()}")

        # 3. TABS for View Options
        tab_summary, tab_raw = st.tabs(["⚡ AI ANALYSIS", "📜 SOURCE DATA"])

        # === TAB 1: AI SUMMARY ===
        with tab_summary:
            st.markdown(f"### 🧠 INTELLIGENCE REPORT")
            
            # Container for streaming text
            report_box = st.empty()
            full_summary = ""

            # Check if we already have the summary in session state to avoid re-generating on tab switch
            # (Simple version: We stream it fresh for effect)
            
            try:
                client = Groq(api_key=api_key)
                stream = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are MEDHA. Summarize the text in 5-7 distinct, professional bullet points. Be concise. Do not use intro phrases like 'Here is the summary'."},
                        {"role": "user", "content": ai_input_text}
                    ],
                    temperature=0.5,
                    max_tokens=600,
                    stream=True
                )

                # Stream the output
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_summary += content
                        report_box.markdown(full_summary + " █")
                
                # Final render without cursor
                report_box.markdown(full_summary)

                st.markdown("---")
                # DOWNLOAD BUTTON (SUMMARY)
                st.download_button(
                    label="💾 Download Summary (.txt)",
                    data=f"MEDHA AI REPORT: {title}\n\n{full_summary}",
                    file_name=f"{title}_Summary.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"AI ERROR: {str(e)}")

        # === TAB 2: RAW DATA ===
        with tab_raw:
            st.markdown(f"### 📂 FULL DOSSIER: {title}")
            
            # DOWNLOAD BUTTON (RAW)
            st.download_button(
                label="💾 Download Raw Data (.txt)",
                data=raw_text,
                file_name=f"{title}_Raw.txt",
                mime="text/plain"
            )
            
            # Show Raw Text (Scrollable area)
            st.text_area("Raw Text Content", raw_text, height=400)

    # ERROR HANDLING
    except wikipedia.exceptions.DisambiguationError as e:
        st.error(f"⚠️ AMBIGUOUS TOPIC. DID YOU MEAN: {', '.join(e.options[:3])}")
    except wikipedia.exceptions.PageError:
        st.error("❌ TOPIC NOT FOUND IN DATABASE.")
    except Exception as e:
        st.error(f"❌ SYSTEM FAILURE: {str(e)}")
