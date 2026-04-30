import streamlit as st
import requests

st.set_page_config(
    page_title="Strategy War Room",
    page_icon="⚔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

WEBHOOK_URL = "https://amanda1818.app.n8n.cloud/webhook/war-room-sim"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.stApp {
    background: #f5f2ed;
    background-image:
        radial-gradient(ellipse 60% 40% at 80% 20%, rgba(180,140,80,0.08), transparent),
        radial-gradient(ellipse 40% 60% at 20% 80%, rgba(30,60,120,0.06), transparent);
    min-height: 100vh;
}

.wr-wrap {
    max-width: 860px;
    margin: 0 auto;
    padding: 64px 32px 100px;
}

.wr-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 5px;
    color: #b8960c;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.wr-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(48px, 7vw, 88px);
    line-height: 0.95;
    color: #0f1f3d;
    margin-bottom: 4px;
    font-weight: 400;
}

.wr-title em {
    font-style: italic;
    color: #1a3a8f;
}

.wr-subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    color: #7a7060;
    letter-spacing: 1px;
    margin-top: 20px;
    font-weight: 300;
}

.wr-rule {
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, #0f1f3d, rgba(180,140,80,0.4), transparent);
    margin: 40px 0 48px;
}

.wr-status {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #fff;
    border: 1px solid #e0d8cc;
    padding: 6px 14px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    color: #5a5040;
    margin-bottom: 48px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.wr-status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #2ecc71;
    box-shadow: 0 0 6px rgba(46,204,113,0.6);
    animation: blink 2s infinite;
    flex-shrink: 0;
}

@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.2; }
}

.wr-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 4px;
    color: #b8960c;
    text-transform: uppercase;
    margin-bottom: 6px;
}

input, textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="base-input"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #ffffff !important;
    border: 1px solid #d5cfc5 !important;
    border-radius: 2px !important;
    color: #0f1f3d !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
}

input:focus, textarea:focus,
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: #1a3a8f !important;
    box-shadow: 0 0 0 3px rgba(26,58,143,0.08) !important;
    outline: none !important;
}

input::placeholder, textarea::placeholder {
    color: #b0a898 !important;
    font-weight: 300 !important;
}

[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="base-input"] {
    background-color: #ffffff !important;
    border-color: #d5cfc5 !important;
    border-radius: 2px !important;
}

.stTextInput label, .stTextArea label { display: none !important; }

.stButton > button {
    background: #0f1f3d !important;
    border: none !important;
    border-radius: 2px !important;
    color: #f5f2ed !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 4px !important;
    padding: 18px 40px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin-top: 8px !important;
    box-shadow: 0 2px 8px rgba(15,31,61,0.2) !important;
}

.stButton > button:hover {
    background: #1a3a8f !important;
    box-shadow: 0 4px 16px rgba(26,58,143,0.3) !important;
}

.wr-gap { margin-bottom: 32px; }
.wr-gap-sm { margin-bottom: 20px; }

.wr-output {
    margin-top: 56px;
    background: #ffffff;
    border: 1px solid #e0d8cc;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    position: relative;
    overflow: hidden;
}

.wr-output-header {
    background: #0f1f3d;
    padding: 14px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.wr-output-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    color: #b8960c;
}

.wr-output-tag {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.3);
}

.wr-output-body {
    padding: 36px 32px;
    font-family: 'DM Sans', sans-serif;
    font-size: 15px;
    line-height: 1.9;
    color: #1a2a4a;
    white-space: pre-wrap;
    border-left: 3px solid #b8960c;
}

.wr-error {
    margin-top: 32px;
    background: #fff8f8;
    border: 1px solid #f0cccc;
    border-left: 3px solid #c0392b;
    padding: 20px 24px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #c0392b;
    letter-spacing: 1px;
    line-height: 1.8;
}

.wr-footer {
    text-align: center;
    margin-top: 80px;
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: #c0b8a8;
    letter-spacing: 4px;
}

[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child { padding-right: 0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="wr-wrap">', unsafe_allow_html=True)

st.markdown("""
<div>
    <div class="wr-eyebrow">⚔ &nbsp; Intelligence Platform &nbsp;/&nbsp; Competitive Strategy</div>
    <div class="wr-title">Strategy<br><em>War Room</em></div>
    <div class="wr-subtitle">Triple-Grounded AI &nbsp;·&nbsp; RAG + Live Market Intelligence + Authority-Filtered News</div>
    <div class="wr-rule"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="wr-status">
    <div class="wr-status-dot"></div>
    ALL SYSTEMS OPERATIONAL &nbsp;·&nbsp; PINECONE ACTIVE &nbsp;·&nbsp; INTEL FEEDS LIVE
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="wr-label">Target Competitor</div>', unsafe_allow_html=True)
    competitor = st.text_input("competitor", placeholder="e.g. Grab", label_visibility="collapsed")
with col2:
    st.markdown('<div class="wr-label">Target Industry</div>', unsafe_allow_html=True)
    industry = st.text_input("industry", placeholder="e.g. Ride-hailing", label_visibility="collapsed")

st.markdown('<div class="wr-gap"></div>', unsafe_allow_html=True)
st.markdown('<div class="wr-label">Client Profile</div>', unsafe_allow_html=True)
client_profile = st.text_input("client_profile", placeholder="e.g. Gojek, SEA ride-hailing, 40% market share in ID/VN", label_visibility="collapsed")

st.markdown('<div class="wr-gap"></div>', unsafe_allow_html=True)
st.markdown('<div class="wr-label">Strategic Scenario</div>', unsafe_allow_html=True)
scenario = st.text_area("scenario", placeholder="e.g. Grab is dropping prices by 10% in Q3 2025. What should Gojek do?", height=150, label_visibility="collapsed")

st.markdown('<div class="wr-gap-sm"></div>', unsafe_allow_html=True)
run = st.button("RUN SIMULATION  →")

if run:
    if not competitor or not scenario:
        st.markdown("""
        <div class="wr-error">
            ⚠ &nbsp; REQUIRED FIELDS MISSING<br>
            Target Competitor and Strategic Scenario are mandatory.
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
                output = (
                    data.get("output")
                    or data.get("text")
                    or data.get("message")
                    or data.get("response")
                    or str(data)
                )
                st.markdown(f"""
                <div class="wr-output">
                    <div class="wr-output-header">
                        <div class="wr-output-label">INTEL REPORT · CONFIDENTIAL</div>
                        <div class="wr-output-tag">TRIPLE-GROUNDED ANALYSIS</div>
                    </div>
                    <div class="wr-output-body">{output}</div>
                </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.Timeout:
                st.markdown("""
                <div class="wr-error">
                    ⚠ &nbsp; REQUEST TIMEOUT (180s)<br>
                    The agent is taking longer than expected. Check n8n execution logs for details.
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="wr-error">
                    ⚠ &nbsp; CONNECTION ERROR<br>{str(e)}
                </div>
                """, unsafe_allow_html=True)

st.markdown("""
<div class="wr-footer">
    STRATEGY WAR ROOM &nbsp;·&nbsp; AMANDA A. APRILIA &nbsp;·&nbsp; CONFIDENTIAL
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
