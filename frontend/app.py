import os
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Focus | AI News Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# Modern Design System — Premium Dark Theme with Accessibility
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg-primary: #0A0E1A;
        --bg-secondary: #111827;
        --bg-card: rgba(17, 24, 39, 0.85);
        --bg-card-hover: rgba(30, 41, 59, 0.9);
        --bg-input: rgba(30, 41, 59, 0.6);
        --border-subtle: rgba(255,255,255,0.06);
        --border-accent: rgba(99,102,241,0.3);
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --accent-indigo: #818CF8;
        --accent-violet: #A78BFA;
        --accent-emerald: #34D399;
        --accent-amber: #FBBF24;
        --accent-rose: #FB7185;
        --accent-sky: #38BDF8;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 20px;
        --shadow-glow: 0 0 20px rgba(99,102,241,0.15);
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.025em;
    }

    /* ===== App Background ===== */
    .stApp {
        background: linear-gradient(180deg, #0A0E1A 0%, #0F1629 50%, #0A0E1A 100%);
        color: var(--text-primary);
    }

    /* ===== Glass Card System ===== */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 24px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.25);
        margin-bottom: 16px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        border-color: rgba(99,102,241,0.15);
        box-shadow: 0 4px 32px rgba(0,0,0,0.35);
    }

    .glass-header {
        background: linear-gradient(135deg, rgba(99,102,241,0.12) 0%, rgba(168,85,247,0.08) 50%, rgba(56,189,248,0.06) 100%);
        border: 1px solid rgba(99,102,241,0.2);
        border-radius: var(--radius-xl);
        padding: 28px 32px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }
    .glass-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(129,140,248,0.5), transparent);
    }

    /* ===== Status Badges ===== */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        white-space: nowrap;
    }
    .badge-pending    { background: rgba(251,191,36,0.12); color: #FBBF24; border: 1px solid rgba(251,191,36,0.3); }
    .badge-published  { background: rgba(52,211,153,0.12); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }
    .badge-approved   { background: rgba(52,211,153,0.12); color: #34D399; border: 1px solid rgba(52,211,153,0.3); }
    .badge-rejected   { background: rgba(251,113,133,0.12); color: #FB7185; border: 1px solid rgba(251,113,133,0.3); }
    .badge-failed     { background: rgba(100,116,139,0.15); color: #94A3B8; border: 1px solid rgba(100,116,139,0.3); }
    .badge-processing { background: rgba(129,140,248,0.12); color: #818CF8; border: 1px solid rgba(129,140,248,0.3); }
    .badge-queued     { background: rgba(56,189,248,0.12);  color: #38BDF8; border: 1px solid rgba(56,189,248,0.3); }

    /* ===== Pipeline Stepper ===== */
    .step-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px 18px;
        border-radius: var(--radius-md);
        margin-bottom: 8px;
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--border-subtle);
        transition: all 0.25s ease;
    }
    .step-active {
        background: rgba(99,102,241,0.1);
        border-color: rgba(99,102,241,0.4);
        box-shadow: 0 0 16px rgba(99,102,241,0.15);
    }
    .step-done {
        background: rgba(16,185,129,0.06);
        border-color: rgba(16,185,129,0.25);
    }
    .step-icon {
        font-size: 1.3rem;
        flex-shrink: 0;
        width: 32px;
        text-align: center;
    }
    .step-label {
        font-size: 0.88rem;
        line-height: 1.35;
    }
    .step-label strong {
        color: var(--text-primary);
    }

    /* ===== Terminal / Logs ===== */
    .terminal-box {
        background: #050810;
        border: 1px solid #1E293B;
        border-radius: var(--radius-md);
        padding: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--accent-sky);
        max-height: 280px;
        overflow-y: auto;
        line-height: 1.55;
    }
    .terminal-line { margin: 3px 0; }

    /* ===== Queue Table ===== */
    .queue-item {
        display: grid;
        grid-template-columns: 40px 1fr 120px 120px 100px;
        align-items: center;
        gap: 12px;
        padding: 14px 18px;
        border-radius: var(--radius-md);
        background: rgba(255,255,255,0.02);
        border: 1px solid var(--border-subtle);
        margin-bottom: 6px;
        font-size: 0.87rem;
        transition: background 0.15s;
    }
    .queue-item:hover {
        background: rgba(255,255,255,0.04);
    }
    .queue-url {
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        color: var(--accent-sky);
    }

    /* ===== Article Preview (Light) ===== */
    .article-preview {
        background: #FFFFFF;
        color: #111827;
        padding: 32px;
        border-radius: var(--radius-md);
        box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    }
    .article-preview h1 {
        font-family: 'Outfit', sans-serif;
        color: #0F172A;
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 12px;
    }
    .article-preview .meta-bar {
        font-size: 0.85rem;
        color: #64748B;
        margin-bottom: 20px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 12px;
    }
    .article-preview .summary-box {
        background: #F8FAFC;
        border-left: 4px solid #6366F1;
        padding: 14px 18px;
        margin-bottom: 24px;
        font-style: italic;
        color: #334155;
    }
    .article-preview .body-text {
        font-size: 1.02rem;
        line-height: 1.7;
        color: #1E293B;
    }

    /* ===== Stat Card ===== */
    .stat-card {
        background: var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-md);
        padding: 20px;
        text-align: center;
    }
    .stat-number {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--accent-indigo), var(--accent-violet));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 4px;
    }

    /* ===== Streamlit widget overrides ===== */
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #F8FAFC;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: rgba(15,22,41,0.6);
        border-radius: var(--radius-md) var(--radius-md) 0 0;
        padding: 6px 6px 0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm) var(--radius-sm) 0 0;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 0.88rem;
    }
    /* Make tab text accessible */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #0D1224 0%, #111827 100%);
    }

    /* Source type icons */
    .source-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 6px;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
    .source-youtube  { background: rgba(255,0,0,0.15); }
    .source-insta    { background: rgba(228,64,95,0.15); }
    .source-tiktok   { background: rgba(0,242,234,0.15); }
    .source-twitter  { background: rgba(29,155,240,0.15); }
    .source-default  { background: rgba(148,163,184,0.15); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# State Initialization
# ==============================================================================
defaults = {
    "active_task_id": None,
    "selected_draft_id": None,
    "task_logs": [],
    "last_created_draft_id": None,
    "queue_tasks": [],       # List of {url, task_id, mode, provider, status, submitted_at}
    "monitoring_task": None,  # Task ID currently being monitored in Jobs tab
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

API_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8000")

# ==============================================================================
# Helper Functions
# ==============================================================================

def detect_source(url: str) -> str:
    """Detect the platform from a URL."""
    url_lower = url.lower()
    if "youtube.com" in url_lower or "youtu.be" in url_lower:
        return "youtube"
    elif "instagram.com" in url_lower:
        return "instagram"
    elif "tiktok.com" in url_lower:
        return "tiktok"
    elif "x.com" in url_lower or "twitter.com" in url_lower:
        return "twitter"
    elif "facebook.com" in url_lower or "fb.watch" in url_lower:
        return "facebook"
    elif "reddit.com" in url_lower:
        return "reddit"
    return "other"

def source_icon(source: str) -> str:
    icons = {
        "youtube": "🎬", "instagram": "📸", "tiktok": "🎵",
        "twitter": "🐦", "facebook": "📘", "reddit": "🔴",
    }
    return icons.get(source, "🔗")

def source_label(source: str) -> str:
    labels = {
        "youtube": "YouTube", "instagram": "Instagram", "tiktok": "TikTok",
        "twitter": "X / Twitter", "facebook": "Facebook", "reddit": "Reddit",
    }
    return labels.get(source, "Web Link")

def fetch_system_stats(base_url: str) -> Optional[Dict[str, Any]]:
    try:
        res = requests.get(f"{base_url}/api/v1/system/stats", timeout=3)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

def fetch_drafts(base_url: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    try:
        param = f"?status={status}" if status and status != "ALL" else ""
        res = requests.get(f"{base_url}/api/v1/drafts{param}", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return []

def fetch_draft_detail(base_url: str, draft_id: int) -> Optional[Dict[str, Any]]:
    try:
        res = requests.get(f"{base_url}/api/v1/drafts/{draft_id}", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

def trigger_curation(
    base_url: str, url: str,
    auto_publish: Optional[bool] = None,
    llm_provider: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """Returns full CurateResponse dict or None."""
    try:
        payload = {"url": url}
        if auto_publish is not None:
            payload["auto_publish"] = auto_publish
        if llm_provider:
            payload["llm_provider"] = llm_provider
        res = requests.post(f"{base_url}/api/v1/curate", json=payload, timeout=10)
        if res.status_code == 202:
            return res.json()
    except Exception as exc:
        st.error(f"Failed to submit URL: {exc}")
    return None

def trigger_batch(base_url: str, urls: List[str], auto_publish, llm_provider) -> Optional[Dict[str, Any]]:
    try:
        payload = {"urls": urls}
        if auto_publish is not None:
            payload["auto_publish"] = auto_publish
        if llm_provider:
            payload["llm_provider"] = llm_provider
        res = requests.post(f"{base_url}/api/v1/curate/batch", json=payload, timeout=30)
        if res.status_code == 202:
            return res.json()
    except Exception as exc:
        st.error(f"Batch submission failed: {exc}")
    return None

def upload_file_batch(base_url: str, file_bytes: bytes, filename: str, auto_publish: bool, llm_provider: str) -> Optional[Dict[str, Any]]:
    try:
        files = {"file": (filename, file_bytes, "text/plain")}
        data = {"auto_publish": str(auto_publish).lower(), "llm_provider": llm_provider or ""}
        res = requests.post(f"{base_url}/api/v1/curate/upload", files=files, data=data, timeout=30)
        if res.status_code == 202:
            return res.json()
    except Exception as exc:
        st.error(f"File upload failed: {exc}")
    return None

def fetch_system_config(base_url: str) -> Optional[Dict[str, Any]]:
    try:
        res = requests.get(f"{base_url}/api/v1/system/config", timeout=4)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None

def update_system_config(base_url: str, data: Dict[str, Any]) -> bool:
    try:
        res = requests.post(f"{base_url}/api/v1/system/config", json=data, timeout=5)
        return res.status_code == 200
    except Exception:
        return False

def poll_task_status(base_url: str, task_id: str) -> Optional[Dict[str, Any]]:
    try:
        res = requests.get(f"{base_url}/api/v1/tasks/{task_id}", timeout=5)
        if res.status_code == 200:
            return res.json()
    except Exception:
        pass
    return None


# ==============================================================================
# Sidebar — Compact System Panel
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 4px;">
            <div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #6366F1, #8B5CF6); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">⚡</div>
            <div>
                <h2 style="margin: 0; font-size: 1.4rem; font-weight: 800; color: #F8FAFC; letter-spacing: -0.03em;">FOCUS</h2>
                <span style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.1em;">AI News Command Center</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    api_url = st.text_input("🔗 Backend URL", value=API_BASE_URL, help="FastAPI server address")

    # Connection status
    stats = fetch_system_stats(api_url)
    if stats:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:8px;margin:8px 0;"><div style="width:8px;height:8px;border-radius:50%;background:#10B981;box-shadow:0 0 8px #10B981;"></div><span style="font-size:0.82rem;font-weight:600;color:#34D399;">Pipeline Online</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:8px;margin:8px 0;"><div style="width:8px;height:8px;border-radius:50%;background:#EF4444;box-shadow:0 0 8px #EF4444;"></div><span style="font-size:0.82rem;font-weight:600;color:#F87171;">Backend Offline</span></div>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ---- Quick Stats ----
    if stats:
        d = stats.get("drafts", {})
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Queued", d.get("pending", 0))
        with c2:
            st.metric("Live", d.get("published", 0))
        with c3:
            st.metric("Failed", d.get("failed", 0))

    st.divider()

    # ---- AI Model Switcher ----
    st.markdown("##### 🤖 AI Engine")
    sys_config = fetch_system_config(api_url)
    current_prov = (sys_config.get("default_llm_provider") or "nvidia_nemotron") if sys_config else "nvidia_nemotron"
    prov_idx = 0 if current_prov == "nvidia_nemotron" else 1

    chosen_model = st.radio(
        "Select Model", ["🤖 NVIDIA Nemotron", "🧠 Gemini 1.5 Pro"],
        index=prov_idx, label_visibility="collapsed",
    )
    active_prov = "nvidia_nemotron" if "NVIDIA" in chosen_model else "gemini"

    if sys_config and active_prov != sys_config.get("default_llm_provider"):
        if st.button("⚡ Apply as Default", use_container_width=True, type="primary"):
            if update_system_config(api_url, {"default_llm_provider": active_prov}):
                st.toast(f"Switched to {chosen_model}!")
                st.rerun()

    # ---- API Keys ----
    with st.expander("🔑 API Credentials", expanded=False):
        st.caption("[Get NVIDIA key](https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b) · [SerpApi key](https://serpapi.com/manage-api-key) · [Gemini key](https://aistudio.google.com/)")
        nv_k = st.text_input("NVIDIA Key", type="password", placeholder="nvapi-..." if not sys_config else (sys_config.get("nvidia_api_key_masked") or "nvapi-..."))
        serp_k = st.text_input("SerpApi Key", type="password", placeholder="Enter key...")
        gem_k = st.text_input("Gemini Key", type="password", placeholder="Enter key...")
        if st.button("💾 Save Keys", use_container_width=True):
            upd = {"default_llm_provider": active_prov}
            if nv_k.strip(): upd["nvidia_api_key"] = nv_k.strip()
            if serp_k.strip(): upd["serpapi_api_key"] = serp_k.strip()
            if gem_k.strip(): upd["gemini_api_key"] = gem_k.strip()
            if update_system_config(api_url, upd):
                st.success("Saved!")
                st.rerun()

    st.divider()

    # ---- Service Status ----
    if stats:
        integ = stats.get("integrations", {})
        services = [
            ("NVIDIA NIM", integ.get("nvidia_configured")),
            ("SerpApi Lens", integ.get("serpapi_configured")),
            ("Gemini AI", integ.get("gemini_configured")),
            ("Laravel API", integ.get("laravel_configured")),
        ]
        for name, ok in services:
            dot = "🟢" if ok else "⚪"
            st.markdown(f"<span style='font-size:0.82rem;'>{dot} {name}</span>", unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()


# ==============================================================================
# Header
# ==============================================================================
model_badge_text = "NVIDIA Nemotron" if active_prov == "nvidia_nemotron" else "Gemini 1.5 Pro"
model_badge_emoji = "🤖" if active_prov == "nvidia_nemotron" else "🧠"
st.markdown(
    f"""
    <div class="glass-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <h1 style="margin: 0; font-size: 2rem; font-weight: 800; background: linear-gradient(90deg, #F8FAFC, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    AI News Command Center
                </h1>
                <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.92rem;">
                    Submit any video link — YouTube, Instagram, TikTok, X, or any URL with video content — and watch the AI curation pipeline transform it into publication-ready news.
                </p>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <span class="badge badge-processing">{model_badge_emoji} {model_badge_text}</span>
                <span class="badge badge-pending">Strict DB Isolation</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# Main Tabs
# ==============================================================================
tab_submit, tab_jobs, tab_review, tab_archive, tab_batch, tab_diag = st.tabs([
    "📥 Submit & Queue",
    "⚡ Active Jobs",
    "✍️ Editorial Desk",
    "📚 Published",
    "📁 Batch Upload",
    "⚙️ System",
])


# ==============================================================================
# TAB 1: Submit & Queue
# ==============================================================================
with tab_submit:
    st.markdown("### 📥 Submit Video Links")
    st.markdown("Paste any video URL from **YouTube**, **Instagram**, **TikTok**, **X/Twitter**, **Facebook**, **Reddit**, or any platform with embeddable video content.")

    # Supported platforms showcase
    st.markdown(
        """
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:20px;">
            <span class="badge" style="background:rgba(255,0,0,0.1); color:#FF4444; border:1px solid rgba(255,0,0,0.25);">🎬 YouTube</span>
            <span class="badge" style="background:rgba(228,64,95,0.1); color:#E4405F; border:1px solid rgba(228,64,95,0.25);">📸 Instagram</span>
            <span class="badge" style="background:rgba(0,242,234,0.1); color:#00F2EA; border:1px solid rgba(0,242,234,0.25);">🎵 TikTok</span>
            <span class="badge" style="background:rgba(29,155,240,0.1); color:#1DA1F2; border:1px solid rgba(29,155,240,0.25);">🐦 X / Twitter</span>
            <span class="badge" style="background:rgba(24,119,242,0.1); color:#1877F2; border:1px solid rgba(24,119,242,0.25);">📘 Facebook</span>
            <span class="badge" style="background:rgba(255,86,0,0.1); color:#FF5700; border:1px solid rgba(255,86,0,0.25);">🔴 Reddit</span>
            <span class="badge" style="background:rgba(148,163,184,0.1); color:#94A3B8; border:1px solid rgba(148,163,184,0.25);">🔗 Any URL</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Input area
    col_url, col_mode, col_go = st.columns([5, 3, 2], gap="small")
    with col_url:
        video_url = st.text_input(
            "Video URL",
            placeholder="https://www.youtube.com/watch?v=... or any video link",
            label_visibility="collapsed",
            key="submit_url",
        )
    with col_mode:
        mode_choice = st.selectbox(
            "Mode", ["🚀 Autonomous (Live Publish)", "✍️ Editorial Review (Draft)"],
            index=0, label_visibility="collapsed", key="submit_mode",
        )
    with col_go:
        submit_btn = st.button("⚡ Queue & Run", type="primary", use_container_width=True, key="submit_btn")

    # Multi-URL textarea
    with st.expander("📝 Paste Multiple URLs (one per line)", expanded=False):
        multi_urls = st.text_area(
            "URLs", height=120,
            placeholder="https://www.youtube.com/watch?v=abc123\nhttps://www.instagram.com/reel/xyz/\nhttps://www.tiktok.com/@user/video/123",
            label_visibility="collapsed", key="multi_urls",
        )
        multi_submit = st.button("⚡ Queue All URLs", use_container_width=True, key="multi_submit_btn")

    # Handle single submit
    if submit_btn and video_url:
        if not video_url.startswith("http"):
            st.error("Please enter a valid URL starting with http:// or https://")
        else:
            is_auto = mode_choice.startswith("🚀")
            resp = trigger_curation(api_url, video_url, auto_publish=is_auto, llm_provider=active_prov)
            if resp:
                src = detect_source(video_url)
                st.session_state.queue_tasks.append({
                    "url": video_url,
                    "task_id": resp["task_id"],
                    "mode": resp.get("mode", "UNKNOWN"),
                    "provider": active_prov,
                    "status": "QUEUED",
                    "source": src,
                    "submitted_at": datetime.now().strftime("%H:%M:%S"),
                })
                st.session_state.active_task_id = resp["task_id"]
                st.toast(f"✅ Queued: {source_label(src)} link submitted!")
                st.rerun()

    # Handle multi submit
    if multi_submit and multi_urls:
        url_list = [u.strip() for u in multi_urls.strip().split("\n") if u.strip()]
        if url_list:
            is_auto = mode_choice.startswith("🚀")
            batch_resp = trigger_batch(api_url, url_list, auto_publish=is_auto, llm_provider=active_prov)
            if batch_resp:
                for task_resp in batch_resp.get("tasks", []):
                    src = detect_source(task_resp["source_url"])
                    st.session_state.queue_tasks.append({
                        "url": task_resp["source_url"],
                        "task_id": task_resp["task_id"],
                        "mode": task_resp.get("mode", "UNKNOWN"),
                        "provider": active_prov,
                        "status": "QUEUED",
                        "source": src,
                        "submitted_at": datetime.now().strftime("%H:%M:%S"),
                    })
                rejected = batch_resp.get("rejected_urls", [])
                st.toast(f"✅ {batch_resp['accepted']} URLs queued" + (f", {len(rejected)} rejected" if rejected else ""))
                st.rerun()

    # ---- Active Queue Display ----
    st.divider()
    st.markdown("### 📋 Submission Queue")

    if not st.session_state.queue_tasks:
        st.info("No links in queue yet. Submit a URL above to get started.")
    else:
        # Header
        st.markdown(
            """
            <div style="display:grid; grid-template-columns:40px 1fr 120px 130px 100px 80px; gap:12px; padding:8px 18px; font-size:0.75rem; color:#64748B; text-transform:uppercase; letter-spacing:0.06em; font-weight:700;">
                <div>#</div><div>URL</div><div>Source</div><div>Mode</div><div>Status</div><div>Action</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        for idx, item in enumerate(reversed(st.session_state.queue_tasks)):
            real_idx = len(st.session_state.queue_tasks) - 1 - idx
            src = item.get("source", "other")
            icon = source_icon(src)
            label = source_label(src)
            status_badge = item.get("status", "QUEUED")
            badge_class = {
                "QUEUED": "badge-queued", "PROCESSING": "badge-processing",
                "COMPLETED": "badge-published", "FAILED": "badge-failed",
            }.get(status_badge, "badge-queued")

            cols = st.columns([0.4, 5, 1.2, 1.3, 1, 0.8])
            with cols[0]:
                st.markdown(f"**{real_idx+1}**")
            with cols[1]:
                st.markdown(f"{icon} `{item['url'][:80]}{'...' if len(item['url']) > 80 else ''}`")
            with cols[2]:
                st.caption(label)
            with cols[3]:
                mode_short = "🚀 Auto" if "AUTO" in item.get("mode", "") else "✍️ Review"
                st.caption(mode_short)
            with cols[4]:
                st.markdown(f"<span class='badge {badge_class}' style='font-size:0.7rem;'>{status_badge}</span>", unsafe_allow_html=True)
            with cols[5]:
                if st.button("👁", key=f"monitor_{real_idx}", help="Monitor this job"):
                    st.session_state.monitoring_task = item["task_id"]
                    st.session_state.active_task_id = item["task_id"]
                    st.session_state.task_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring task: {item['task_id']}"]


# ==============================================================================
# TAB 2: Active Jobs — Live Pipeline Monitor
# ==============================================================================
with tab_jobs:
    st.markdown("### ⚡ Active Pipeline Jobs")
    st.markdown("Real-time view of currently running AI curation pipelines. Select a job from the queue to see detailed step-by-step progress.")

    active_id = st.session_state.active_task_id

    if not active_id:
        # Show all queued tasks with status polling
        if st.session_state.queue_tasks:
            st.markdown("#### 📊 Job Status Overview")
            for idx, item in enumerate(reversed(st.session_state.queue_tasks)):
                task_info = poll_task_status(api_url, item["task_id"])
                state = task_info.get("state", "PENDING") if task_info else "UNKNOWN"
                prog = task_info.get("progress", 0) if task_info else 0
                details = task_info.get("details", "") if task_info else ""
                stage = task_info.get("stage", "") if task_info else ""

                # Update queue status
                real_idx = len(st.session_state.queue_tasks) - 1 - idx
                if state == "SUCCESS":
                    st.session_state.queue_tasks[real_idx]["status"] = "COMPLETED"
                elif state == "FAILURE":
                    st.session_state.queue_tasks[real_idx]["status"] = "FAILED"
                elif state == "PROGRESS":
                    st.session_state.queue_tasks[real_idx]["status"] = "PROCESSING"

                src = item.get("source", "other")
                with st.container():
                    c1, c2, c3 = st.columns([3, 5, 2])
                    with c1:
                        st.markdown(f"**{source_icon(src)} {source_label(src)}**")
                        st.caption(f"`{item['task_id'][:12]}...`")
                    with c2:
                        st.progress(prog / 100.0, text=f"{stage}: {details[:60]}" if details else f"Progress: {prog}%")
                    with c3:
                        if st.button("🔍 Monitor", key=f"job_mon_{idx}", use_container_width=True):
                            st.session_state.active_task_id = item["task_id"]
                            st.session_state.task_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring: {item['task_id']}"]
                            st.rerun()
                    st.divider()
        else:
            st.info("No active jobs. Submit URLs in the **Submit & Queue** tab.")
    else:
        # Full pipeline monitor for selected task
        curr_task_id = active_id
        st.markdown(f"#### 🎯 Monitoring Job: `{curr_task_id[:16]}...`")

        col_stop, _ = st.columns([2, 6])
        with col_stop:
            if st.button("← Back to Job List", use_container_width=True):
                st.session_state.active_task_id = None
                st.rerun()

        progress_bar = st.empty()
        status_banner = st.empty()
        col_stages, col_terminal = st.columns([1, 1], gap="large")
        stages_container = col_stages.empty()
        terminal_container = col_terminal.empty()

        is_done = False
        iteration = 0

        while not is_done and iteration < 60:
            iteration += 1
            task_info = poll_task_status(api_url, curr_task_id)

            if not task_info:
                status_banner.warning("⏳ Waiting for Celery worker heartbeat...")
                time.sleep(1.5)
                continue

            state = task_info.get("state")
            stage = task_info.get("stage") or "INITIALIZING"
            prog = task_info.get("progress", 0)
            details = task_info.get("details", "")

            progress_bar.progress(prog / 100.0, text=f"{details} ({prog}%)")

            timestamp = datetime.now().strftime("%H:%M:%S")
            log_line = f"[{timestamp}] [{stage}] {details}"
            if not st.session_state.task_logs or st.session_state.task_logs[-1] != log_line:
                st.session_state.task_logs.append(log_line)

            # Pipeline stepper
            def get_step(step_name, target_stage, current_prog, step_min):
                if current_prog >= step_min + 20:
                    return "step-row step-done", "✅"
                elif target_stage == step_name:
                    return "step-row step-active", "🔄"
                return "step-row", "⚪"

            task_mode = task_info.get("mode", "")
            is_auto = "AUTONOMOUS" in task_mode

            s1c, s1i = get_step("DOWNLOADING", stage, prog, 15)
            s2c, s2i = get_step("EXTRACTING_MEDIA", stage, prog, 35)
            s3c, s3i = get_step("SEARCHING_CONTEXT", stage, prog, 55)

            task_prov = task_info.get("provider", "") or active_prov
            prov_name = "NVIDIA Nemotron" if "nvidia" in task_prov else "Gemini 1.5 Pro"

            if is_auto:
                s4c, s4i = get_step("AI_CURATING", stage, prog, 70)
                s5c, s5i = get_step("PUBLISHING", stage, prog, 85)
                s4_lbl = f"<strong>4. AI Curation ({prov_name}):</strong> Schema hydration & synthesis"
                s5_lbl = "<strong>5. Publishing:</strong> Laravel API insertion & alerts"
                mode_badge = f"<span class='badge badge-published'>AUTONOMOUS</span>"
            else:
                s4c, s4i = get_step("GENERATING_ARTICLE", stage, prog, 75)
                s5c, s5i = get_step("SAVING_DRAFT", stage, prog, 90)
                s4_lbl = f"<strong>4. AI Draft ({prov_name}):</strong> Multimodal synthesis"
                s5_lbl = "<strong>5. Saving:</strong> SQLite review queue"
                mode_badge = f"<span class='badge badge-pending'>EDITORIAL REVIEW</span>"

            stages_html = f"""
            <div class="glass-card" style="padding:18px;">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                    <h4 style="margin:0;font-size:1rem;">Pipeline Stages</h4>
                    {mode_badge}
                </div>
                <div class="{s1c}"><span class="step-icon">{s1i}</span><div class="step-label"><strong>1. Acquisition:</strong> yt-dlp video download</div></div>
                <div class="{s2c}"><span class="step-icon">{s2i}</span><div class="step-label"><strong>2. Media Slicing:</strong> ffmpeg audio & keyframes</div></div>
                <div class="{s3c}"><span class="step-icon">{s3i}</span><div class="step-label"><strong>3. Context:</strong> Google Lens reverse search</div></div>
                <div class="{s4c}"><span class="step-icon">{s4i}</span><div class="step-label">{s4_lbl}</div></div>
                <div class="{s5c}"><span class="step-icon">{s5i}</span><div class="step-label">{s5_lbl}</div></div>
            </div>
            """
            stages_container.markdown(stages_html, unsafe_allow_html=True)

            terminal_lines = "".join([f"<div class='terminal-line'>{l}</div>" for l in st.session_state.task_logs[-12:]])
            terminal_html = f"""
            <div class="glass-card" style="padding:18px;">
                <h4 style="margin:0 0 14px 0;font-size:1rem;">Live Worker Output</h4>
                <div class="terminal-box">{terminal_lines}</div>
            </div>
            """
            terminal_container.markdown(terminal_html, unsafe_allow_html=True)

            if state == "SUCCESS":
                is_done = True
                result = task_info.get("result", {})
                draft_id = result.get("draft_id")
                st.session_state.last_created_draft_id = draft_id
                st.session_state.selected_draft_id = draft_id
                res_mode = result.get("mode", "")

                # Update queue
                for qi in st.session_state.queue_tasks:
                    if qi["task_id"] == curr_task_id:
                        qi["status"] = "COMPLETED"

                if res_mode == "AUTONOMOUS":
                    pub_res = result.get("publish_result", {})
                    news_id = pub_res.get("news_id", "LIVE")
                    status_banner.success(f"🚀 **Published!** News ID: **#{news_id}** — _{result.get('headline')}_")
                else:
                    status_banner.success(f"🎉 **Draft Created!** #{draft_id}: _{result.get('headline')}_")

            elif state == "FAILURE":
                is_done = True
                for qi in st.session_state.queue_tasks:
                    if qi["task_id"] == curr_task_id:
                        qi["status"] = "FAILED"
                status_banner.error(f"❌ **Failed:** {task_info.get('error')}")

            time.sleep(1.5)


# ==============================================================================
# TAB 3: Editorial Desk
# ==============================================================================
with tab_review:
    st.markdown("### ✍️ Editorial Review & Approval")
    st.markdown("Inspect AI-curated content, verify evidence, edit articles, and push approved drafts to production.")

    col_flt, col_srch, col_rel = st.columns([3, 4, 1])
    with col_flt:
        status_filter = st.selectbox("Filter", ["PENDING", "ALL", "PUBLISHED", "REJECTED", "FAILED"], index=0, key="ed_filter")
    with col_srch:
        search_q = st.text_input("Search", placeholder="Filter by headline or location...", key="ed_search")
    with col_rel:
        st.write("")
        st.write("")
        if st.button("🔄", use_container_width=True, key="ed_refresh"):
            st.rerun()

    all_drafts = fetch_drafts(api_url, status=status_filter)
    if search_q:
        q = search_q.lower()
        all_drafts = [d for d in all_drafts if q in (d.get("headline") or "").lower() or q in (d.get("location") or "").lower()]

    if not all_drafts:
        st.info("No drafts found. Run the pipeline in **Submit & Queue** to generate content.")
    else:
        draft_opts = {f"#{d['id']} | {d.get('headline') or 'Untitled'} [{d['status']}]": d['id'] for d in all_drafts}
        default_idx = 0
        if st.session_state.selected_draft_id:
            for i, (lbl, did) in enumerate(draft_opts.items()):
                if did == st.session_state.selected_draft_id:
                    default_idx = i
                    break

        sel_label = st.selectbox("Select Draft", list(draft_opts.keys()), index=default_idx, key="ed_select")
        sel_id = draft_opts[sel_label]
        st.session_state.selected_draft_id = sel_id

        draft = fetch_draft_detail(api_url, sel_id)
        if draft:
            st.divider()
            col_ev, col_ed = st.columns([1, 1], gap="large")

            # LEFT: Evidence
            with col_ev:
                st.markdown("#### 📸 Evidence & Media")

                st.markdown(
                    f"""<div class="glass-card" style="padding:16px;">
                        <span style="font-size:0.78rem;color:#64748B;text-transform:uppercase;">Source</span><br>
                        <a href="{draft['source_url']}" target="_blank" style="color:#38BDF8;word-break:break-all;font-weight:500;">{draft['source_url']} ↗</a>
                    </div>""",
                    unsafe_allow_html=True,
                )

                c_b1, c_b2 = st.columns(2)
                with c_b1:
                    bcls = f"badge-{draft['status'].lower()}"
                    st.markdown(f"<span class='badge {bcls}'>{draft['status']}</span>", unsafe_allow_html=True)
                with c_b2:
                    score = draft.get("confidence_score") or 0.0
                    sc_color = "#10B981" if score >= 0.85 else ("#F59E0B" if score >= 0.7 else "#EF4444")
                    st.markdown(f"<div style='text-align:right;'><span style='color:#94A3B8;font-size:0.82rem;'>AI Confidence: </span><strong style='color:{sc_color};font-size:1.1rem;'>{int(score*100)}%</strong></div>", unsafe_allow_html=True)
                    st.progress(score)

                media = draft.get("media_paths") or {}
                kf = media.get("keyframes", [])
                if kf:
                    st.markdown("##### Keyframes")
                    kcols = st.columns(len(kf))
                    for i, fp in enumerate(kf):
                        with kcols[i]:
                            if os.path.exists(fp):
                                st.image(fp, caption=f"Frame {i+1}", use_column_width=True)
                            else:
                                st.caption(f"Frame {i+1}: `{os.path.basename(fp)}`")

                af = media.get("audio_path")
                if af and os.path.exists(af):
                    st.markdown("##### Audio")
                    st.audio(af)

                st.markdown("##### 🔍 Context & Location")
                st.markdown(
                    f"""<div class="glass-card">
                        <div style="margin-bottom:8px;">
                            <span style="color:#64748B;font-size:0.82rem;">Location:</span><br>
                            <strong style="color:#38BDF8;">📍 {draft.get('location') or 'Unspecified'}</strong>
                        </div>
                        <div>
                            <span style="color:#64748B;font-size:0.82rem;">AI Notes:</span>
                            <p style="margin:4px 0 0;color:#CBD5E1;font-size:0.88rem;line-height:1.5;">{draft.get('ai_notes') or 'No notes.'}</p>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )

                if draft.get("laravel_post_id"):
                    st.success(f"✅ Live on Laravel (Post ID: `{draft['laravel_post_id']}`)")

            # RIGHT: Editor
            with col_ed:
                st.markdown("#### 📰 Article Editor")

                cat_c, loc_c = st.columns(2)
                with cat_c:
                    cat = st.selectbox(
                        "Category",
                        ["1 - Local News", "2 - Breaking News", "3 - Politics", "4 - Civic", "5 - Sports", "6 - Weather", "7 - Entertainment", "8 - Technology"],
                        index=0, key="ed_cat",
                    )
                    cat_id = int(cat.split(" - ")[0])
                with loc_c:
                    ed_loc = st.text_input("Location", value=draft.get("location") or "", key="ed_loc")

                ed_head = st.text_input("Headline", value=draft.get("headline") or "", key="ed_head")
                st.caption(f"{len(ed_head)} chars · recommended 60-90")

                ed_sum = st.text_area("Summary", value=draft.get("summary") or "", height=80, key="ed_sum")

                tags_list = draft.get("tags") or []
                ed_tags = st.text_input("Tags (comma-separated)", value=", ".join(tags_list), key="ed_tags")

                tab_edit, tab_prev = st.tabs(["💻 HTML Editor", "👁️ Preview"])
                with tab_edit:
                    ed_body = st.text_area("HTML Body", value=draft.get("body_content") or "", height=240, key="ed_body")
                with tab_prev:
                    st.markdown(
                        f"""<div class="article-preview">
                            <span style="color:#6366F1;font-weight:700;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em;">{cat.split(' - ')[1]} · 📍 {ed_loc}</span>
                            <h1>{ed_head}</h1>
                            <div class="meta-bar">Curated on {datetime.now().strftime('%B %d, %Y')} · AI Verified</div>
                            <div class="summary-box">{ed_sum}</div>
                            <div class="body-text">{ed_body}</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                b1, b2, b3 = st.columns([1, 1.5, 1])
                with b1:
                    if st.button("💾 Save", use_container_width=True, key="ed_save"):
                        upd = {
                            "headline": ed_head, "summary": ed_sum,
                            "location": ed_loc, "tags": [t.strip() for t in ed_tags.split(",") if t.strip()],
                            "body_content": ed_body,
                        }
                        r = requests.patch(f"{api_url}/api/v1/drafts/{sel_id}", json=upd)
                        if r.status_code == 200:
                            st.success("Saved!")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"Error: {r.text}")
                with b2:
                    is_pub = draft["status"] == "PUBLISHED"
                    if st.button("✅ Published" if is_pub else "🚀 Approve & Publish", type="primary", disabled=is_pub, use_container_width=True, key="ed_pub"):
                        with st.spinner("Pushing to Laravel..."):
                            r = requests.post(f"{api_url}/api/v1/drafts/{sel_id}/publish?category_id={cat_id}")
                        if r.status_code == 200:
                            st.balloons()
                            st.success(f"Live! Post ID: {r.json().get('laravel_post_id')}")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"Failed: {r.text}")
                with b3:
                    is_rej = draft["status"] in ["REJECTED", "PUBLISHED"]
                    if st.button("❌ Reject", disabled=is_rej, use_container_width=True, key="ed_rej"):
                        r = requests.post(f"{api_url}/api/v1/drafts/{sel_id}/reject")
                        if r.status_code == 200:
                            st.warning("Rejected.")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(f"Error: {r.text}")


# ==============================================================================
# TAB 4: Published Archive
# ==============================================================================
with tab_archive:
    st.markdown("### 📚 Published Articles")
    st.markdown("All news articles successfully pushed to the live production platform.")

    published = fetch_drafts(api_url, status="PUBLISHED")
    if not published:
        st.info("No published articles yet. Approve drafts in the **Editorial Desk** tab.")
    else:
        for p in published:
            src = detect_source(p.get("source_url", ""))
            st.markdown(
                f"""
                <div class="glass-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div style="flex:1;">
                            <div style="display:flex;gap:8px;align-items:center;margin-bottom:8px;">
                                <span class="badge badge-published">Published</span>
                                <span style="color:#64748B;font-size:0.82rem;">Post #{p.get('laravel_post_id') or 'N/A'}</span>
                                <span style="color:#64748B;font-size:0.82rem;">· {source_icon(src)} {source_label(src)}</span>
                            </div>
                            <h3 style="margin:0 0 6px;color:#F8FAFC;font-size:1.15rem;">{p.get('headline')}</h3>
                            <p style="margin:0;color:#94A3B8;font-size:0.85rem;">📍 {p.get('location') or 'Local'} · <a href="{p.get('source_url')}" target="_blank" style="color:#60A5FA;">{p.get('source_url','')[:60]}...</a></p>
                        </div>
                        <div style="text-align:right;flex-shrink:0;">
                            <span style="font-size:0.85rem;color:#10B981;font-weight:700;">{int((p.get('confidence_score') or 0)*100)}%</span>
                        </div>
                    </div>
                    <div style="background:rgba(0,0,0,0.2);border-radius:8px;padding:12px;margin-top:10px;color:#CBD5E1;font-size:0.88rem;">
                        {p.get('summary') or 'No summary available.'}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==============================================================================
# TAB 5: Batch Upload
# ==============================================================================
with tab_batch:
    st.markdown("### 📁 Batch URL Upload")
    st.markdown("Upload a `.txt` or `.csv` file containing one video URL per line. All URLs will be queued simultaneously for AI curation.")

    st.markdown(
        """
        <div class="glass-card" style="padding:20px;">
            <h4 style="margin:0 0 10px;">📋 File Format Guide</h4>
            <div style="font-size:0.88rem;color:#CBD5E1;line-height:1.6;">
                <strong>Text file (.txt):</strong> One URL per line<br>
                <strong>CSV file (.csv):</strong> URL in the first column<br>
                <strong>Comments:</strong> Lines starting with <code>#</code> are ignored<br>
                <strong>Supported platforms:</strong> YouTube, Instagram, TikTok, X/Twitter, Facebook, Reddit, any URL
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_upload, col_opts = st.columns([2, 1])
    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload URL file",
            type=["txt", "csv"],
            help="Text or CSV file with one URL per line",
            key="batch_file",
        )
    with col_opts:
        batch_mode = st.selectbox("Mode", ["🚀 Autonomous", "✍️ Editorial Review"], key="batch_mode")
        batch_prov = st.selectbox("AI Engine", ["🤖 NVIDIA Nemotron", "🧠 Gemini 1.5 Pro"], key="batch_prov")

    if uploaded_file:
        file_content = uploaded_file.read()
        try:
            text_preview = file_content.decode("utf-8")
        except UnicodeDecodeError:
            text_preview = file_content.decode("latin-1")

        lines = [l.strip() for l in text_preview.split("\n") if l.strip() and not l.strip().startswith("#")]
        url_count = len(lines)

        st.markdown(f"**📊 Found {url_count} URLs in uploaded file:**")

        with st.expander(f"Preview ({min(url_count, 20)} of {url_count} URLs)", expanded=True):
            for i, line in enumerate(lines[:20]):
                if "," in line:
                    line = line.split(",")[0].strip()
                src = detect_source(line)
                st.markdown(f"`{i+1}.` {source_icon(src)} `{line}`")
            if url_count > 20:
                st.caption(f"...and {url_count - 20} more")

        if st.button("🚀 Upload & Queue All", type="primary", use_container_width=True, key="batch_go"):
            is_auto = batch_mode.startswith("🚀")
            prov = "nvidia_nemotron" if "NVIDIA" in batch_prov else "gemini"
            result = upload_file_batch(api_url, file_content, uploaded_file.name, is_auto, prov)
            if result:
                for t in result.get("tasks", []):
                    src = detect_source(t["source_url"])
                    st.session_state.queue_tasks.append({
                        "url": t["source_url"],
                        "task_id": t["task_id"],
                        "mode": t.get("mode", "UNKNOWN"),
                        "provider": prov,
                        "status": "QUEUED",
                        "source": src,
                        "submitted_at": datetime.now().strftime("%H:%M:%S"),
                    })
                rejected = result.get("rejected_urls", [])
                st.success(f"✅ **{result['accepted']}** URLs queued successfully!")
                if rejected:
                    st.warning(f"⚠️ {len(rejected)} URLs rejected: {', '.join(rejected[:5])}")
                st.rerun()


# ==============================================================================
# TAB 6: System & Config
# ==============================================================================
with tab_diag:
    st.markdown("### ⚙️ System Configuration & Diagnostics")

    diag_stats = fetch_system_stats(api_url)

    # Stats cards
    if diag_stats:
        d = diag_stats.get("drafts", {})
        s = diag_stats.get("storage", {})

        c1, c2, c3, c4, c5 = st.columns(5)
        cards = [
            (c1, str(d.get("total", 0)), "Total Drafts"),
            (c2, str(d.get("pending", 0)), "Pending"),
            (c3, str(d.get("published", 0)), "Published"),
            (c4, str(d.get("failed", 0)), "Failed"),
            (c5, f"{s.get('size_mb', 0)} MB", "Disk Cache"),
        ]
        for col, num, lbl in cards:
            with col:
                st.markdown(
                    f"""<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{lbl}</div></div>""",
                    unsafe_allow_html=True,
                )

    st.divider()

    col_health, col_cache = st.columns(2, gap="large")

    with col_health:
        st.markdown("#### 🏥 Service Health")
        if diag_stats:
            st.json(diag_stats)
        else:
            st.error("Cannot reach backend.")

    with col_cache:
        st.markdown("#### 🧹 Cache Management")
        st.markdown("Temporary video/audio/keyframe files accumulate during pipeline runs. Purge them after articles are published.")

        if diag_stats:
            storage = diag_stats.get("storage", {})
            st.metric("Cached Files", f"{storage.get('file_count', 0)} files")
            st.metric("Disk Used", f"{storage.get('size_mb', 0)} MB")

        if st.button("🧹 Purge Temp Media", type="secondary", key="diag_clean"):
            try:
                r = requests.post(f"{api_url}/api/v1/system/cleanup", timeout=5)
                if r.status_code == 200:
                    data = r.json()
                    st.success(f"Purged {data.get('deleted_files')} files ({data.get('freed_mb')} MB freed)")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    st.error(f"Failed: {r.text}")
            except Exception as e:
                st.error(f"Error: {e}")

        st.divider()
        st.markdown("#### 📊 Queue Session Stats")
        q = st.session_state.queue_tasks
        total_q = len(q)
        completed_q = sum(1 for x in q if x.get("status") == "COMPLETED")
        failed_q = sum(1 for x in q if x.get("status") == "FAILED")
        active_q = total_q - completed_q - failed_q

        st.markdown(f"**Total Submitted:** {total_q}")
        st.markdown(f"**Completed:** {completed_q}")
        st.markdown(f"**Active/Queued:** {active_q}")
        st.markdown(f"**Failed:** {failed_q}")

        if st.button("🗑️ Clear Session Queue", key="clear_queue"):
            st.session_state.queue_tasks = []
            st.session_state.active_task_id = None
            st.toast("Queue cleared!")
            st.rerun()
