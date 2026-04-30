import streamlit as st
import requests
import time

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Strategy War Room",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── YOUR N8N WEBHOOK URL ──────────────────────────────────────────────────────
WEBHOOK_URL = https://amanda1818.app.n8n.cloud/webhook/war-room-sim

# ── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Share+Tech+Mono&family=Inter:wght@300;400;500&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp {
    background-color: #040d1a;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,80,200,0.15), transparent),
        repeating-linear-gradient(0deg, transparent, transparent 40px, rgba(0,150,255,0.02) 40px, rgba(0,150,255,0.02) 41px),
        repeating-linear-gradient(90deg, transparent, transparent 40px, rgba(0,150,255,0.02) 40px, rgba(0,150,255,0.02) 41px);
    min-height: 100vh;
}

/* hide streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── SCAN LINE OVERLAY ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.08) 2px,
        rgba(0,0,0,0.08) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── MAIN WRAPPER ── */
.war-room-wrapper {
    max-width: 900px;
    margin: 0 auto;
    padding: 48px 24px 80px;
}

/* ── HEADER ── */
.header-block {
    text-align: center;
    margin-bottom: 56px;
    position: relative;
}

.classified-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    letter-spacing: 6px;
    color: #ff3b3b;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.classified-tag::before,
.classified-tag::after {
    content: '';
    width: 40px;
    height: 1px;
    background: #ff3b3b;
    opacity: 0.6;
}

.main-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(42px, 8vw, 86px);
    line-height: 0.92;
    color: #ffffff;
    letter-spacing: 2px;
    text-shadow:
        0 0 40px rgba(0,120,255,0.4),
        0 0 80px rgba(0,80,200,0.2);
    margin-bottom: 6px;
}

.main-title span {
    color: #1a6eff;
}

.subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    color: rgba(255,255,255,0.35);
    letter-spacing: 3px;
    margin-top: 16px;
}

.header-line {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(26,110,255,0.5), transparent);
    margin-top: 32px;
}

/* ── STATUS BAR ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 40px;
    padding: 10px 16px;
    border: 1px solid rgba(26,110,255,0.15);
    background: rgba(26,110,255,0.04);
    font-family: 'Share Tech Mono', monospace;
    font-size: 11px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 2px;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #00ff88;
    box-shadow: 0 0 8px #00ff88;
    animation: pulse 2s infinite;
    flex-shrink: 0;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── FORM SECTION ── */
.section-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    color: #1a6eff;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(26,110,255,0.25);
}

/* ── INPUT OVERRIDES ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(26,110,255,0.25) !important;
    border-radius: 0 !important;
    color: #e8f0ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 14px !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    caret-color: #1a6eff !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: rgba(26,110,255,0.7) !important;
    box-shadow: 0 0 0 1px rgba(26,110,255,0.3), inset 0 0 20px rgba(26,110,255,0.04) !important;
    outline: none !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: rgba(255,255,255,0.18) !important;
    font-style: normal !important;
}

/* hide streamlit labels (we use our own) */
.stTextInput label, .stTextArea label { display: none !important; }

/* ── BUTTON ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #1a6eff !important;
    border-radius: 0 !important;
    color: #1a6eff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 13px !important;
    letter-spacing: 4px !important;
    padding: 16px 40px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    position: relative !important;
    overflow: hidden !important;
    margin-top: 8px !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: rgba(26,110,255,0.08);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.3s ease;
}

.stButton > button:hover {
    background: rgba(26,110,255,0.1) !important;
    box-shadow: 0 0 20px rgba(26,110,255,0.25) !important;
    color: #ffffff !important;
}

.stButton > button:hover::before { transform: scaleX(1); }

/* ── DIVIDER ── */
.field-gap { margin-bottom: 28px; }

/* ── OUTPUT PANEL ── */
.output-panel {
    margin-top: 48px;
    border: 1px solid rgba(26,110,255,0.2);
    background: rgba(10,20,40,0.6);
    padding: 32px;
    position: relative;
}

.output-panel::before {
    content: 'INTEL REPORT';
    position: absolute;
    top: -1px;
    left: 32px;
    background: #1a6eff;
    color: #ffffff;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    padding: 4px 12px;
}

.output-panel::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 32px; height: 32px;
    border-top: 2px solid #1a6eff;
    border-right: 2px solid #1a6eff;
}

.output-text {
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    line-height: 1.8 !important;
    color: rgba(220,235,255,0.9) !important;
    white-space: pre-wrap !important;
}

/* ── ERROR PANEL ── */
.error-panel {
    margin-top: 32px;
    border: 1px solid rgba(255,59,59,0.3);
    background: rgba(255,59,59,0.05);
    padding: 20px 24px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
    color: #ff6b6b;
    letter-spacing: 1px;
}

/* ── LOADING ── */
.stSpinner > div {
    border-color: #1a6eff transparent transparent transparent !important;
}

/* ── FOOTER ── */
.war-room-footer {
    text-align: center;
    margin-top: 64px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    color: rgba(255,255,255,0.12);
    letter-spacing: 3px;
}

/* ── COLUMNS ── */
[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child { padding-right: 0 !important; }

</style>
""", unsafe_allow_html=True)

# ── LAYOUT ────────────────────────────────────────────────────────────────────
st.markdown('<div class="war-room-wrapper">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-block">
    <div class="classified-tag">✕ &nbsp; CLASSIFIED &nbsp; ✕</div>
    <div class="main-title">STRATEGY<br><span>WAR ROOM</span></div>
    <div class="subtitle">COMPETITOR RESPONSE SIMULATOR &nbsp;·&nbsp; TRIPLE-GROUNDED AI</div>
    <div class="header-line"></div>
</div>
""", unsafe_allow_html=True)

# Status bar
st.markdown("""
<div class="status-bar">
    <div class="status-dot"></div>
    SYSTEM ONLINE &nbsp;·&nbsp; RAG ENGINE ACTIVE &nbsp;·&nbsp; INTEL FEEDS CONNECTED
</div>
""", unsafe_allow_html=True)

# ── FORM ──────────────────────────────────────────────────────────────────────

# Row 1: two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-label">TARGET COMPETITOR</div>', unsafe_allow_html=True)
    competitor = st.text_input("competitor", placeholder="e.g. Grab", label_visibility="collapsed")

with col2:
    st.markdown('<div class="section-label">TARGET INDUSTRY</div>', unsafe_allow_html=True)
    industry = st.text_input("industry", placeholder="e.g. ride-hailing", label_visibility="collapsed")

st.markdown('<div class="field-gap"></div>', unsafe_allow_html=True)

# Client profile
st.markdown('<div class="section-label">CLIENT PROFILE</div>', unsafe_allow_html=True)
client_profile = st.text_input("client_profile", placeholder="e.g. Gojek, SEA ride-hailing, 40% market share in ID/VN", label_visibility="collapsed")

st.markdown('<div class="field-gap"></div>', unsafe_allow_html=True)

# Scenario
st.markdown('<div class="section-label">STRATEGIC SCENARIO</div>', unsafe_allow_html=True)
scenario = st.text_area("scenario", placeholder="e.g. Grab is dropping prices by 10% in Q3 2025. What should we do?", height=140, label_visibility="collapsed")

st.markdown('<div class="field-gap"></div>', unsafe_allow_html=True)

# Button
run = st.button("✕  RUN SIMULATION")

# ── EXECUTION ─────────────────────────────────────────────────────────────────
if run:
    if not competitor or not scenario:
        st.markdown("""
        <div class="error-panel">
            ⚠ &nbsp; MISSING REQUIRED FIELDS — TARGET COMPETITOR AND SCENARIO ARE MANDATORY
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Gathering intelligence across all three data sources..."):
            payload = {
                "client_profile": client_profile,
                "competitor": competitor,
                "industry": industry,
                "scenario": scenario
            }
            try:
                response = requests.post(WEBHOOK_URL, json=payload, timeout=180)
                response.raise_for_status()
                data = response.json()

                # n8n returns the agent output in different keys depending on setup
                output = (
                    data.get("output")
                    or data.get("text")
                    or data.get("message")
                    or data.get("response")
                    or str(data)
                )

                st.markdown(f"""
                <div class="output-panel">
                    <div class="output-text">{output}</div>
                </div>
                """, unsafe_allow_html=True)

            except requests.exceptions.Timeout:
                st.markdown("""
                <div class="error-panel">
                    ⚠ &nbsp; REQUEST TIMEOUT — THE AGENT IS STILL PROCESSING. REFRESH AND TRY A SIMPLER SCENARIO FIRST.
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-panel">
                    ⚠ &nbsp; CONNECTION ERROR — {str(e).upper()}
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="war-room-footer">
    STRATEGY WAR ROOM &nbsp;·&nbsp; BUILT BY AMANDA A. APRILIA &nbsp;·&nbsp; CONFIDENTIAL
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
