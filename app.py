import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Strategy War Room",
    page_icon="⚔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

WEBHOOK_URL = "https://amanda1818.app.n8n.cloud/webhook/war-room-sim"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

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

.wr-wrap { max-width: 1000px; margin: 0 auto; padding: 56px 32px 100px; }

.wr-eyebrow { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 5px; color: #b8960c; margin-bottom: 16px; }
.wr-title { font-family: 'DM Serif Display', serif; font-size: clamp(44px, 6vw, 80px); line-height: 0.95; color: #0f1f3d; font-weight: 400; }
.wr-title em { font-style: italic; color: #1a3a8f; }
.wr-subtitle { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #7a7060; letter-spacing: 1px; margin-top: 16px; font-weight: 300; }
.wr-rule { width: 100%; height: 1px; background: linear-gradient(90deg, #0f1f3d, rgba(180,140,80,0.4), transparent); margin: 36px 0 44px; }

.wr-status { display: inline-flex; align-items: center; gap: 8px; background: #fff; border: 1px solid #e0d8cc; padding: 6px 14px; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 2px; color: #5a5040; margin-bottom: 40px; box-shadow: 0 1px 4px rgba(0,0,0,0.05); }
.wr-status-dot { width: 6px; height: 6px; border-radius: 50%; background: #2ecc71; box-shadow: 0 0 6px rgba(46,204,113,0.6); animation: blink 2s infinite; flex-shrink: 0; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }

/* MODE TABS */
.mode-tabs { display: flex; gap: 0; margin-bottom: 40px; border: 1px solid #d5cfc5; overflow: hidden; }
.mode-tab { flex: 1; padding: 14px; text-align: center; font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 3px; cursor: pointer; transition: all 0.2s; }
.mode-tab-active { background: #0f1f3d; color: #f5f2ed; }
.mode-tab-inactive { background: #fff; color: #7a7060; }

.wr-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 4px; color: #b8960c; margin-bottom: 6px; }

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
input::placeholder, textarea::placeholder { color: #b0a898 !important; font-weight: 300 !important; }
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="base-input"] {
    background-color: #ffffff !important; border-color: #d5cfc5 !important; border-radius: 2px !important;
}
.stTextInput label, .stTextArea label { display: none !important; }

.stButton > button {
    background: #0f1f3d !important; border: none !important; border-radius: 2px !important;
    color: #f5f2ed !important; font-family: 'DM Mono', monospace !important;
    font-size: 11px !important; letter-spacing: 4px !important; padding: 18px 40px !important;
    width: 100% !important; cursor: pointer !important; transition: all 0.2s !important;
    margin-top: 8px !important; box-shadow: 0 2px 8px rgba(15,31,61,0.2) !important;
}
.stButton > button:hover { background: #1a3a8f !important; box-shadow: 0 4px 16px rgba(26,58,143,0.3) !important; }

.wr-gap { margin-bottom: 28px; }
.wr-gap-sm { margin-bottom: 16px; }
.wr-section-divider { width: 100%; height: 1px; background: rgba(180,140,80,0.2); margin: 40px 0 32px; }

/* OUTPUT CARDS */
.wr-card {
    background: #ffffff; border: 1px solid #e0d8cc;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04); margin-bottom: 20px;
    overflow: hidden;
}
.wr-card-header {
    background: #0f1f3d; padding: 12px 24px;
    display: flex; align-items: center; justify-content: space-between;
}
.wr-card-title { font-family: 'DM Mono', monospace; font-size: 10px; letter-spacing: 3px; color: #b8960c; }
.wr-card-badge { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; color: rgba(255,255,255,0.3); }
.wr-card-body { padding: 24px; font-family: 'DM Sans', sans-serif; font-size: 14px; line-height: 1.8; color: #1a2a4a; border-left: 3px solid #b8960c; }

/* METRIC GRID */
.metric-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; padding: 20px 24px; }
.metric-item { text-align: center; padding: 16px; background: #f9f7f4; border: 1px solid #ede8e0; }
.metric-value { font-family: 'DM Serif Display', serif; font-size: 28px; color: #0f1f3d; font-weight: 400; }
.metric-value.red { color: #c0392b; }
.metric-value.green { color: #27ae60; }
.metric-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; color: #7a7060; margin-top: 4px; }

/* OPTIONS TABLE */
.options-table { width: 100%; border-collapse: collapse; font-family: 'DM Sans', sans-serif; font-size: 13px; }
.options-table th { background: #f5f2ed; padding: 10px 16px; text-align: left; font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; color: #7a7060; border-bottom: 1px solid #e0d8cc; }
.options-table td { padding: 12px 16px; border-bottom: 1px solid #f0ebe3; color: #1a2a4a; vertical-align: top; }
.risk-low { color: #27ae60; font-weight: 600; }
.risk-med { color: #f39c12; font-weight: 600; }
.risk-high { color: #c0392b; font-weight: 600; }

/* STRATEGY MAP */
.strategy-map { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; padding: 20px 24px; }
.strategy-map-item { padding: 16px; border-left: 3px solid; }
.sm-financial { border-color: #1a3a8f; background: rgba(26,58,143,0.04); }
.sm-customer { border-color: #b8960c; background: rgba(184,150,12,0.04); }
.sm-process { border-color: #27ae60; background: rgba(39,174,96,0.04); }
.sm-learning { border-color: #8e44ad; background: rgba(142,68,173,0.04); }
.sm-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 2px; color: #7a7060; margin-bottom: 6px; }
.sm-content { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #1a2a4a; font-weight: 500; }

/* OKR */
.okr-item { padding: 16px 24px; border-bottom: 1px solid #f0ebe3; }
.okr-objective { font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 600; color: #0f1f3d; margin-bottom: 8px; }
.okr-kr { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #5a6a8a; padding: 4px 0 4px 16px; border-left: 2px solid #b8960c; margin: 4px 0; }

/* SCENARIO COMPARISON */
.scenario-col { background: #fff; border: 1px solid #e0d8cc; padding: 20px; margin-bottom: 16px; }
.scenario-label { font-family: 'DM Mono', monospace; font-size: 9px; letter-spacing: 3px; color: #b8960c; margin-bottom: 12px; }

.wr-error { margin-top: 24px; background: #fff8f8; border: 1px solid #f0cccc; border-left: 3px solid #c0392b; padding: 16px 20px; font-family: 'DM Mono', monospace; font-size: 11px; color: #c0392b; letter-spacing: 1px; line-height: 1.8; }
.wr-footer { text-align: center; margin-top: 80px; font-family: 'DM Mono', monospace; font-size: 9px; color: #c0b8a8; letter-spacing: 4px; }

[data-testid="column"] { padding: 0 8px !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child { padding-right: 0 !important; }

/* RADIO BUTTON OVERRIDE */
.stRadio label { font-family: 'DM Mono', monospace !important; font-size: 11px !important; letter-spacing: 2px !important; }
</style>
""", unsafe_allow_html=True)

# ── HELPERS ──────────────────────────────────────────────────────────────────

def call_agent(payload):
    response = requests.post(WEBHOOK_URL, json=payload, timeout=180)
    response.raise_for_status()
    data = response.json()
    raw = data.get("output") or data.get("text") or data.get("message") or str(data)
    try:
        cleaned = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned), raw
    except:
        return None, raw

def risk_class(r):
    r = str(r).upper()
    if r == "LOW": return "risk-low"
    if r == "HIGH": return "risk-high"
    return "risk-med"

def _source_row(icon, label, source):
    if isinstance(source, dict):
        tier = source.get('credibility', '?')
        tier_color = '#27ae60' if tier == 'TIER 1' else '#f39c12' if tier == 'TIER 2' else '#7a7060'
        finding = source.get('finding', 'No data')
        reason = source.get('reason', '')
        return f'''{icon} <strong style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:2px">{label}</strong>
        <span style="color:{tier_color};font-family:DM Mono,monospace;font-size:9px;font-weight:600"> [{tier}]</span>
        — {finding}<br>
        <span style="font-size:11px;color:#9a9080;padding-left:20px">{reason}</span>'''
    return f'{icon} {label}: {source}'
def render_output(parsed, raw):
    if not parsed:
        st.markdown(f"""
        <div class="wr-card">
            <div class="wr-card-header"><div class="wr-card-title">INTEL REPORT</div></div>
            <div class="wr-card-body" style="white-space:pre-wrap">{raw}</div>
        </div>""", unsafe_allow_html=True)
        return

    threat = parsed.get("threat_assessment", {})
    opts = parsed.get("strategic_options", [])
    rec = parsed.get("recommended_action", {})
    sm = rec.get("strategy_map", {})
    okrs = rec.get("okrs", [])
    actions = rec.get("immediate_actions_30_days", [])
    sources = parsed.get("data_sources_used", {})
    gaps = parsed.get("data_gaps", [])

    # Situation
    st.markdown(f"""
    <div class="wr-card">
        <div class="wr-card-header">
            <div class="wr-card-title">01 · SITUATION ASSESSMENT</div>
            <div class="wr-card-badge">CONFIDENCE: {parsed.get('confidence_score', '?')}/10</div>
        </div>
        <div class="wr-card-body">{parsed.get('situation', '')}</div>
    </div>""", unsafe_allow_html=True)

    # Threat metrics
    st.markdown(f"""
    <div class="wr-card">
        <div class="wr-card-header">
            <div class="wr-card-title">02 · THREAT QUANTIFICATION</div>
            <div class="wr-card-badge">{threat.get('confidence', '')} CONFIDENCE</div>
        </div>
        <div class="metric-grid">
            <div class="metric-item">
                <div class="metric-value red">{threat.get('market_share_at_risk_pct', '?')}%</div>
                <div class="metric-label">MARKET SHARE AT RISK</div>
            </div>
            <div class="metric-item">
                <div class="metric-value red">${threat.get('estimated_revenue_impact_usd_millions', '?')}M</div>
                <div class="metric-label">REVENUE AT RISK (USD)</div>
            </div>
            <div class="metric-item">
                <div class="metric-value">{parsed.get('confidence_score', '?')}<span style="font-size:16px">/10</span></div>
                <div class="metric-label">DATA CONFIDENCE SCORE</div>
            </div>
        </div>
        <div style="padding:12px 24px;background:#fff8f0;border-top:1px solid #ede8e0">
            <span style="font-family:DM Mono,monospace;font-size:9px;letter-spacing:2px;color:#c0392b">
            ⚠ DO NOTHING IMPACT:</span>
            <span style="font-family:DM Serif Display,serif;font-size:20px;color:#c0392b;margin-left:12px">
            ${threat.get('do_nothing_impact_usd_millions','?')}M</span>
            <span style="font-family:DM Mono,monospace;font-size:9px;color:#9a9080;margin-left:8px">
            PROJECTED LOSS IF NO ACTION TAKEN</span>
        </div>
        <div class="wr-card-body">
            {threat.get('summary', '')}<br><br>
            <strong style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px">
            CALCULATION METHODOLOGY:</strong><br>
            <span style="font-size:13px;color:#5a6a8a">{threat.get('calculation_methodology', 'Not provided')}</span><br><br>
            <strong style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px">
            CONFIDENCE RATIONALE:</strong><br>
            <span style="font-size:13px;color:#5a6a8a">{threat.get('confidence_reason', 'Not provided')}</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # Options table
    rows = ""
    for o in opts:
        rows += f"""
        <tr>
            <td><strong>{o.get('name','')}</strong><br><span style="color:#7a7060;font-size:12px">{o.get('description','')}</span></td>
            <td>${o.get('revenue_impact_usd_millions','?')}M<br>
            <span style="font-size:11px;color:#27ae60">ROI: {o.get('roi_pct','?')}%</span></td>
            <td>{o.get('payback_period_months','?')} mo<br>
            <span style="font-size:11px;color:#7a7060">Cost: ${o.get('implementation_cost_usd_millions','?')}M</span></td>
            <td class="{risk_class(o.get('risk_rating',''))}">{o.get('risk_rating','')}</td>
            <td style="font-size:11px;color:#7a7060">{o.get('data_source_used','')}<br>
            <span style="color:#5a6a8a;font-style:italic">{o.get('roi_calculation','')[:80]}...</span></td>
        </tr>"""

    st.markdown(f"""
    <div class="wr-card">
        <div class="wr-card-header"><div class="wr-card-title">03 · STRATEGIC OPTIONS COMPARISON</div></div>
        <div style="padding:0 0 0 3px;border-left:3px solid #b8960c">
        <table class="options-table">
            <thead><tr>
                <th>OPTION</th><th>REVENUE IMPACT</th>
                <th>PAYBACK</th><th>RISK</th><th>DATA SOURCE</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
        </div>
    </div>""", unsafe_allow_html=True)

    # Recommended + 30-day actions
    action_items = "".join([f"<li style='margin:4px 0'>{a}</li>" for a in actions])
    st.markdown(f"""
    <div class="wr-card">
        <div class="wr-card-header"><div class="wr-card-title">04 · RECOMMENDED ACTION</div></div>
        <div class="wr-card-body">
            <strong>Decision:</strong> {rec.get('option', '')}<br><br>
            <strong style="font-family:DM Mono,monospace;font-size:11px;letter-spacing:2px">
            IMMEDIATE ACTIONS — NEXT 30 DAYS:</strong>
            <ul style="margin-top:10px;padding-left:20px">{action_items}</ul>
        </div>
    </div>""", unsafe_allow_html=True)

    # Strategy Map
    st.markdown(f"""
    <div class="wr-card">
        <div class="wr-card-header"><div class="wr-card-title">05 · BALANCED SCORECARD STRATEGY MAP</div></div>
        <div class="strategy-map">
            <div class="strategy-map-item sm-financial">
                <div class="sm-label">FINANCIAL PERSPECTIVE</div>
                <div class="sm-content">{sm.get('financial', '')}</div>
            </div>
            <div class="strategy-map-item sm-customer">
                <div class="sm-label">CUSTOMER PERSPECTIVE</div>
                <div class="sm-content">{sm.get('customer', '')}</div>
            </div>
            <div class="strategy-map-item sm-process">
                <div class="sm-label">INTERNAL PROCESS</div>
                <div class="sm-content">{sm.get('internal_process', '')}</div>
            </div>
            <div class="strategy-map-item sm-learning">
                <div class="sm-label">LEARNING & GROWTH</div>
                <div class="sm-content">{sm.get('learning_growth', '')}</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    # OKRs
    okr_html = ""
    for okr in okrs:
        krs = "".join([f'<div class="okr-kr">→ {kr}</div>' for kr in okr.get("key_results", [])])
        okr_html += f"""
        <div class="okr-item">
            <div class="okr-objective">🎯 {okr.get('objective','')}</div>
            {krs}
        </div>"""

    st.markdown(f"""
    <div class="wr-card">
        <div class="wr-card-header"><div class="wr-card-title">06 · OKR FRAMEWORK</div></div>
        <div style="border-left:3px solid #b8960c">{okr_html}</div>
    </div>""", unsafe_allow_html=True)

    # Data sources & gaps
    gap_html = "".join([f"<li style='margin:4px 0;color:#c0392b'>{g}</li>" for g in gaps])
    st.markdown(f"""
    <div class="wr-card">
        <div class="wr-card-header"><div class="wr-card-title">07 · INTELLIGENCE AUDIT</div></div>
        <div class="wr-card-body">
            <strong style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px">DATA RETRIEVED:</strong><br>
            {_source_row('📁', 'ANNUAL REPORT', sources.get('annual_report_lookup', {}))}<br>
            {_source_row('📊', 'FINANCIAL TELEMETRY', sources.get('financial_telemetry_search', {}))}<br>
            {_source_row('📰', 'INDUSTRY NEWS', sources.get('trusted_industry_news', {}))}<br>
            {_source_row('🔍', 'GAP SEARCH', sources.get('gap_intelligence_search', {}))}<br><br>
            <strong style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px">
            OVERALL DATA QUALITY:</strong>
            <span style="font-weight:600;color:#1a3a8f"> {parsed.get('overall_data_quality','?')}</span>
            — {parsed.get('data_quality_rationale','')}<br><br>
            <strong style="font-family:DM Mono,monospace;font-size:10px;letter-spacing:2px">DATA GAPS (ACTION REQUIRED):</strong>
            <ul style="margin-top:8px;padding-left:20px">{gap_html}</ul>
        </div>
    </div>""", unsafe_allow_html=True)


# ── LAYOUT ────────────────────────────────────────────────────────────────────
st.markdown('<div class="wr-wrap">', unsafe_allow_html=True)

st.markdown("""
<div>
    <div class="wr-eyebrow">⚔ Intelligence Platform &nbsp;/&nbsp; Competitive Strategy</div>
    <div class="wr-title">Strategy<br><em>War Room</em></div>
    <div class="wr-subtitle">Triple-Grounded AI · RAG + Live Market Intelligence + Authority-Filtered News</div>
    <div class="wr-rule"></div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="wr-status">
    <div class="wr-status-dot"></div>
    ALL SYSTEMS OPERATIONAL &nbsp;·&nbsp; PINECONE ACTIVE &nbsp;·&nbsp; INTEL FEEDS LIVE
</div>""", unsafe_allow_html=True)

# ── MODE SELECTOR ─────────────────────────────────────────────────────────────
mode = st.radio(
    "Mode",
    ["SINGLE SCENARIO", "SCENARIO COMPARISON (3 OPTIONS)"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown('<div class="wr-gap-sm"></div>', unsafe_allow_html=True)

# ── SHARED FIELDS ─────────────────────────────────────────────────────────────
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

# ── MODE: SINGLE ──────────────────────────────────────────────────────────────
if mode == "SINGLE SCENARIO":
    st.markdown('<div class="wr-label">Strategic Scenario</div>', unsafe_allow_html=True)
    scenario = st.text_area("scenario", placeholder="e.g. Grab is dropping prices by 10% in Q3 2025. What should Gojek do?", height=130, label_visibility="collapsed")
    st.markdown('<div class="wr-gap-sm"></div>', unsafe_allow_html=True)
    run = st.button("RUN SIMULATION  →")

    if run:
        if not competitor or not scenario:
            st.markdown('<div class="wr-error">⚠ TARGET COMPETITOR and STRATEGIC SCENARIO are required.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Querying annual reports, financial telemetry, and industry intelligence..."):
                try:
                    parsed, raw = call_agent({
                        "client_profile": client_profile,
                        "competitor": competitor,
                        "industry": industry,
                        "scenario": scenario
                    })
                    st.markdown('<div class="wr-section-divider"></div>', unsafe_allow_html=True)
                    render_output(parsed, raw)
                except requests.exceptions.Timeout:
                    st.markdown('<div class="wr-error">⚠ TIMEOUT — Agent is processing. Check n8n execution logs.</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="wr-error">⚠ CONNECTION ERROR — {str(e)}</div>', unsafe_allow_html=True)

# ── MODE: COMPARISON ──────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="font-family:'DM Mono',monospace;font-size:10px;letter-spacing:2px;color:#7a7060;margin-bottom:20px;padding:12px 16px;background:#fff;border:1px solid #e0d8cc">
        Enter 3 different strategic scenarios — the agent will run all 3 and output a side-by-side comparison.
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="wr-label">SCENARIO A</div>', unsafe_allow_html=True)
        s1 = st.text_area("s1", placeholder="e.g. Match Grab's 10% price cut", height=120, label_visibility="collapsed")
    with c2:
        st.markdown('<div class="wr-label">SCENARIO B</div>', unsafe_allow_html=True)
        s2 = st.text_area("s2", placeholder="e.g. Launch loyalty program instead", height=120, label_visibility="collapsed")
    with c3:
        st.markdown('<div class="wr-label">SCENARIO C</div>', unsafe_allow_html=True)
        s3 = st.text_area("s3", placeholder="e.g. Expand to new city to offset loss", height=120, label_visibility="collapsed")

    st.markdown('<div class="wr-gap-sm"></div>', unsafe_allow_html=True)
    run_comp = st.button("RUN ALL 3 SCENARIOS  →")

    if run_comp:
        if not competitor or not s1 or not s2 or not s3:
            st.markdown('<div class="wr-error">⚠ Fill in Target Competitor and all 3 Scenarios.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="wr-section-divider"></div>', unsafe_allow_html=True)
            scenarios = [("A", s1), ("B", s2), ("C", s3)]
            results = []

            for label, sc in scenarios:
                with st.spinner(f"Running Scenario {label}..."):
                    try:
                        parsed, raw = call_agent({
                            "client_profile": client_profile,
                            "competitor": competitor,
                            "industry": industry,
                            "scenario": sc
                        })
                        results.append((label, sc, parsed, raw))
                    except Exception as e:
                        results.append((label, sc, None, str(e)))

            # Comparison summary table
            st.markdown("""
            <div class="wr-card">
                <div class="wr-card-header"><div class="wr-card-title">SCENARIO COMPARISON — EXECUTIVE SUMMARY</div></div>""",
            unsafe_allow_html=True)

            comp_rows = ""
            for label, sc, parsed, raw in results:
                if parsed:
                    threat = parsed.get("threat_assessment", {})
                    opts = parsed.get("strategic_options", [])
                    rec_opt = parsed.get("recommended_action", {}).get("option", "")[:80]
                    best = min(opts, key=lambda x: x.get("payback_period_months", 999)) if opts else {}
                    comp_rows += f"""
                    <tr>
                        <td><strong>Scenario {label}</strong><br><span style="font-size:12px;color:#7a7060">{sc[:60]}...</span></td>
                        <td class="risk-high">${threat.get('estimated_revenue_impact_usd_millions','?')}M</td>
                        <td>{best.get('payback_period_months','?')} months</td>
                        <td class="{risk_class(best.get('risk_rating',''))}">{best.get('risk_rating','?')}</td>
                        <td style="font-size:12px">{rec_opt}</td>
                    </tr>"""
                else:
                    comp_rows += f"<tr><td>Scenario {label}</td><td colspan='4' style='color:#c0392b'>Error: {raw[:60]}</td></tr>"

            st.markdown(f"""
                <div style="padding:0 0 0 3px;border-left:3px solid #b8960c">
                <table class="options-table">
                    <thead><tr>
                        <th>SCENARIO</th><th>REVENUE AT RISK</th>
                        <th>FASTEST PAYBACK</th><th>RISK</th><th>RECOMMENDED MOVE</th>
                    </tr></thead>
                    <tbody>{comp_rows}</tbody>
                </table>
                </div>
            </div>""", unsafe_allow_html=True)

            # Full breakdown per scenario
            for label, sc, parsed, raw in results:
                st.markdown(f"""
                <div style="margin-top:40px;font-family:'DM Mono',monospace;font-size:11px;
                letter-spacing:4px;color:#b8960c;border-bottom:1px solid #e0d8cc;padding-bottom:12px;margin-bottom:24px">
                    SCENARIO {label} — FULL BREAKDOWN
                </div>""", unsafe_allow_html=True)
                render_output(parsed, raw)

st.markdown("""
<div class="wr-footer">
    STRATEGY WAR ROOM &nbsp;·&nbsp; AMANDA A. APRILIA &nbsp;·&nbsp; CONFIDENTIAL
</div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
