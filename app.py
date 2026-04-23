import streamlit as st
import requests
import json
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Strategy War Room",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

  /* ── Root variables ── */
  :root {
    --bg-void:      #060b14;
    --bg-panel:     #0b1524;
    --bg-card:      #0f1e35;
    --border:       #1b3050;
    --border-glow:  #1e5fa8;
    --accent:       #2a7fd4;
    --accent-dim:   #1a4f87;
    --amber:        #d4862a;
    --amber-dim:    #8a4f0f;
    --text-primary: #c8ddf5;
    --text-muted:   #4d6a8a;
    --text-bright:  #e8f4ff;
    --red-alert:    #c0392b;
    --green-go:     #1a7a4a;
  }

  /* ── Global reset ── */
  html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-void) !important;
    font-family: 'IBM Plex Sans', sans-serif;
    color: var(--text-primary);
  }

  [data-testid="stHeader"] { background: transparent !important; }
  [data-testid="stToolbar"] { display: none !important; }
  [data-testid="stSidebar"] { display: none !important; }
  footer { display: none !important; }

  /* ── Scanline overlay ── */
  [data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(0, 20, 50, 0.15) 2px,
      rgba(0, 20, 50, 0.15) 4px
    );
    pointer-events: none;
    z-index: 9999;
  }

  /* ── Main container ── */
  .block-container {
    max-width: 960px !important;
    padding: 2.5rem 2rem !important;
  }

  /* ── Header ── */
  .war-room-header {
    text-align: center;
    margin-bottom: 2.5rem;
    position: relative;
  }
  .war-room-header::before {
    content: "⚔  CLASSIFIED  ⚔";
    display: block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.45em;
    color: var(--red-alert);
    margin-bottom: 0.6rem;
    opacity: 0.85;
  }
  .war-room-header h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    letter-spacing: 0.06em;
    color: var(--text-bright);
    line-height: 1.05;
    margin: 0;
    text-shadow:
      0 0 40px rgba(42, 127, 212, 0.45),
      0 0 80px rgba(42, 127, 212, 0.15);
  }
  .war-room-header .subtitle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.25em;
    color: var(--text-muted);
    margin-top: 0.5rem;
  }
  .header-rule {
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      var(--border-glow) 30%,
      var(--accent) 50%,
      var(--border-glow) 70%,
      transparent 100%
    );
    margin: 1.2rem auto 0;
    width: 70%;
  }

  /* ── Section labels ── */
  .section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  /* ── Textarea ── */
  .stTextArea textarea {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text-primary) !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.7 !important;
    resize: vertical !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
  }
  .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(42, 127, 212, 0.18) !important;
    outline: none !important;
  }
  .stTextArea textarea::placeholder { color: var(--text-muted) !important; }
  .stTextArea label { display: none !important; }

  /* ── Button ── */
  .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--accent-dim) 0%, var(--accent) 100%) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 4px !important;
    color: #fff !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.25rem !important;
    letter-spacing: 0.2em !important;
    padding: 0.65rem 2rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.4) !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, var(--accent) 0%, #3d9ef0 100%) !important;
    box-shadow: 0 0 20px rgba(42, 127, 212, 0.4) !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button:active { transform: translateY(0) !important; }

  /* ── Spinner ── */
  .stSpinner > div {
    border-top-color: var(--accent) !important;
  }
  [data-testid="stSpinner"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    color: var(--text-muted) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.15em !important;
  }

  /* ── Intelligence Brief card ── */
  .intel-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 4px;
    padding: 1.8rem 2rem;
    margin-top: 1.8rem;
    position: relative;
    overflow: hidden;
  }
  .intel-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, var(--accent) 0%, transparent 60%);
  }
  .intel-card-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
  }
  .intel-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.25em;
    color: var(--amber);
    background: rgba(212, 134, 42, 0.1);
    border: 1px solid var(--amber-dim);
    border-radius: 2px;
    padding: 0.2rem 0.5rem;
  }
  .intel-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 0.1em;
    color: var(--text-bright);
    flex: 1;
  }
  .intel-timestamp {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
  }
  .intel-body {
    font-size: 0.93rem;
    line-height: 1.8;
    color: var(--text-primary);
    white-space: pre-wrap;
    word-wrap: break-word;
  }
  .intel-body strong { color: var(--text-bright); }

  /* ── Error card ── */
  .error-card {
    background: rgba(192, 57, 43, 0.08);
    border: 1px solid rgba(192, 57, 43, 0.35);
    border-left: 3px solid var(--red-alert);
    border-radius: 4px;
    padding: 1.2rem 1.5rem;
    margin-top: 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #e07070;
    letter-spacing: 0.04em;
  }
  .error-card::before {
    content: "⚠  TRANSMISSION ERROR";
    display: block;
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    color: var(--red-alert);
    margin-bottom: 0.5rem;
  }

  /* ── Status bar ── */
  .status-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    color: var(--text-muted);
  }
  .status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--green-go);
    box-shadow: 0 0 6px var(--green-go);
    animation: pulse 2s infinite;
    flex-shrink: 0;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
  }
</style>
""", unsafe_allow_html=True)

# ── WEBHOOK ───────────────────────────────────────────────────────────────────
WEBHOOK_URL = "https://timorbuild.app.n8n.cloud/webhook-test/war-room-sim"

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="war-room-header">
  <h1>Strategy War Room<br>Competitor Response Simulator</h1>
  <p class="subtitle">Real-time competitive intelligence &amp; scenario modelling</p>
  <div class="header-rule"></div>
</div>
""", unsafe_allow_html=True)

# ── INPUT SECTION ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Strategic Proposal</div>', unsafe_allow_html=True)

proposal = st.text_area(
    label="proposal",
    placeholder='e.g. "We are dropping prices by 10% across our premium SKUs to pressure Competitor X out of the mid-market segment."',
    height=180,
)

run = st.button("⚔  Run Simulation")

# ── SIMULATION ────────────────────────────────────────────────────────────────
if run:
    if not proposal.strip():
        st.markdown("""
        <div class="error-card">
          No strategic proposal detected. Input required before simulation can proceed.
        </div>""", unsafe_allow_html=True)
    else:
        with st.spinner("Analysing competitive landscape... please stand by"):
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps({"chatInput": proposal}),
                    timeout=60,
                )
                response.raise_for_status()

                # Try to extract text from response
                try:
                    data = response.json()
                    # n8n may return {"output": "..."} or {"text": "..."} or a list
                    if isinstance(data, list) and len(data) > 0:
                        data = data[0]
                    brief_text = (
                        data.get("output")
                        or data.get("text")
                        or data.get("message")
                        or data.get("response")
                        or json.dumps(data, indent=2)
                    )
                except Exception:
                    brief_text = response.text

                timestamp = time.strftime("%Y-%m-%d  %H:%M:%S UTC", time.gmtime())

                st.markdown(f"""
                <div class="intel-card">
                  <div class="intel-card-header">
                    <span class="intel-badge">TOP SECRET</span>
                    <span class="intel-title">Intelligence Brief</span>
                    <span class="intel-timestamp">{timestamp}</span>
                  </div>
                  <div class="intel-body">{brief_text}</div>
                </div>
                """, unsafe_allow_html=True)

            except requests.exceptions.Timeout:
                st.markdown("""
                <div class="error-card">
                  Request timed out after 60 seconds. The simulation endpoint may be unavailable or overloaded.
                </div>""", unsafe_allow_html=True)
            except requests.exceptions.ConnectionError as e:
                st.markdown(f"""
                <div class="error-card">
                  Connection failed. Verify the webhook URL is active and reachable.<br><br>{e}
                </div>""", unsafe_allow_html=True)
            except requests.exceptions.HTTPError as e:
                st.markdown(f"""
                <div class="error-card">
                  HTTP {response.status_code} — {e}
                </div>""", unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-card">
                  Unexpected error: {e}
                </div>""", unsafe_allow_html=True)

# ── STATUS BAR ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="status-bar">
  <span class="status-dot"></span>
  <span>SECURE CHANNEL ACTIVE</span>
  <span>|</span>
  <span>ENDPOINT: timorbuild.app.n8n.cloud</span>
  <span>|</span>
  <span>ENCRYPTION: TLS 1.3</span>
</div>
""", unsafe_allow_html=True)
