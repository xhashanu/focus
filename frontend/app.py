import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
import streamlit as st

# ==============================================================================
# Page Configuration & Global Theme
# ==============================================================================
st.set_page_config(
    page_title="Focus | AI News Curation Studio",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Modern Cyberpunk / Dark Glassmorphic Design System
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.02em;
    }

    /* Overall background */
    .stApp {
        background-color: #0B0F19;
        color: #F1F5F9;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(18, 24, 38, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }

    .glass-header {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }

    /* Status Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-pending {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-published {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-rejected {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    .badge-failed {
        background: rgba(100, 116, 139, 0.2);
        color: #94A3B8;
        border: 1px solid rgba(100, 116, 139, 0.4);
    }

    /* Pipeline Step Tracker */
    .pipeline-step {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        transition: all 0.2s ease;
    }
    .step-active {
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.5);
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.2);
    }
    .step-done {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    /* Terminal logs box */
    .terminal-box {
        background-color: #06090F;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 14px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #38BDF8;
        max-height: 220px;
        overflow-y: auto;
    }
    .terminal-line {
        margin: 4px 0;
        line-height: 1.4;
    }

    /* Article Preview Mockup */
    .article-preview {
        background: #FFFFFF;
        color: #111827;
        padding: 32px;
        border-radius: 12px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .article-preview h1 {
        font-family: 'Outfit', sans-serif;
        color: #0F172A;
        font-size: 1.8rem;
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
        font-size: 1.05rem;
        line-height: 1.7;
        color: #1E293B;
    }

    /* Streamlit widget tweaks */
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #F8FAFC;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# State Initialization
# ==============================================================================
if "active_task_id" not in st.session_state:
    st.session_state.active_task_id = None
if "selected_draft_id" not in st.session_state:
    st.session_state.selected_draft_id = None
if "task_logs" not in st.session_state:
    st.session_state.task_logs = []
if "last_created_draft_id" not in st.session_state:
    st.session_state.last_created_draft_id = None

# Base URL
API_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8000")

# ==============================================================================
# Helper Functions
# ==============================================================================
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
    base_url: str,
    url: str,
    auto_publish: Optional[bool] = None,
    llm_provider: Optional[str] = None,
) -> Optional[str]:
    try:
        payload = {"url": url}
        if auto_publish is not None:
            payload["auto_publish"] = auto_publish
        if llm_provider:
            payload["llm_provider"] = llm_provider
        res = requests.post(f"{base_url}/api/v1/curate", json=payload, timeout=10)
        if res.status_code == 202:
            return res.json().get("task_id")
    except Exception as exc:
        st.error(f"Failed to submit URL: {exc}")
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
# Sidebar - System Control & Status
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
            <span style="font-size: 2rem;">⚡</span>
            <div>
                <h2 style="margin: 0; font-size: 1.3rem; font-weight: 800; color: #F8FAFC;">FOCUS</h2>
                <span style="font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em;">AI News Curation Studio</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Multimodal Video-to-News Pipeline & Review Desk")

    api_url = st.text_input("Backend API Address", value=API_BASE_URL)

    stats = fetch_system_stats(api_url)

    if stats:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #10B981; box-shadow: 0 0 8px #10B981;"></div>
                <span style="font-size: 0.85rem; font-weight: 600; color: #34D399;">Backend & Pipeline Online</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 8px; margin: 10px 0;">
                <div style="width: 10px; height: 10px; border-radius: 50%; background: #EF4444; box-shadow: 0 0 8px #EF4444;"></div>
                <span style="font-size: 0.85rem; font-weight: 600; color: #F87171;">FastAPI Offline / Disconnected</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Draft Counts & Storage
    st.markdown("#### 📊 Queue Snapshot")
    if stats:
        drafts_info = stats.get("drafts", {})
        storage_info = stats.get("storage", {})

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Pending", drafts_info.get("pending", 0), help="Drafts awaiting human review")
        with col_m2:
            st.metric("Published", drafts_info.get("published", 0), help="Pushed to live Laravel app")

        st.caption(f"💾 Temp Cache: **{storage_info.get('size_mb', 0)} MB** ({storage_info.get('file_count', 0)} files)")
    else:
        st.info("System stats unavailable.")

    st.divider()

    # AI Model Switcher & API Configuration
    st.markdown("#### 🤖 AI Model & APIs")
    sys_config = fetch_system_config(api_url)
    current_default_prov = (sys_config.get("default_llm_provider") or "nvidia_nemotron") if sys_config else "nvidia_nemotron"

    model_idx = 0 if current_default_prov == "nvidia_nemotron" else 1
    chosen_sidebar_model = st.radio(
        "Active LLM Provider",
        options=["🤖 NVIDIA Nemotron", "🧠 Gemini 1.5 Pro"],
        index=model_idx,
        help="Model used for AI curation and schema hydration.",
    )
    active_prov_code = "nvidia_nemotron" if "NVIDIA" in chosen_sidebar_model else "gemini"

    # Quick Switch button if radio changed from saved setting
    if sys_config and active_prov_code != sys_config.get("default_llm_provider"):
        if st.button("⚡ Set as Default Model", use_container_width=True):
            if update_system_config(api_url, {"default_llm_provider": active_prov_code}):
                st.toast(f"Active model switched to {chosen_sidebar_model}!")
                st.rerun()

    # API Keys Configuration Expander
    with st.expander("🔑 Manage API Keys (Free)", expanded=False):
        st.markdown(
            """
            <div style='font-size:0.75rem; color:#94A3B8; margin-bottom:8px;'>
            Get free keys below:<br>
            • <a href='https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b' target='_blank' style='color:#38BDF8;'>NVIDIA Nemotron (Free API)</a><br>
            • <a href='https://serpapi.com/manage-api-key' target='_blank' style='color:#38BDF8;'>SerpApi Google Lens (Free Tier)</a><br>
            • <a href='https://aistudio.google.com/' target='_blank' style='color:#38BDF8;'>Google Gemini API</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        nv_key_input = st.text_input(
            "NVIDIA API Key",
            type="password",
            placeholder=sys_config.get("nvidia_api_key_masked", "Enter nvapi-...") if sys_config else "Enter key...",
            help="Get free trial credits from https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b",
        )
        serp_key_input = st.text_input(
            "SerpApi Key (Google Lens)",
            type="password",
            placeholder=sys_config.get("serpapi_api_key_masked", "Enter SerpApi key...") if sys_config else "Enter key...",
            help="Free key from https://serpapi.com/manage-api-key",
        )
        gem_key_input = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder=sys_config.get("gemini_api_key_masked", "Enter Gemini key...") if sys_config else "Enter key...",
        )
        if st.button("💾 Save API Credentials", use_container_width=True):
            update_data = {"default_llm_provider": active_prov_code}
            if nv_key_input.strip():
                update_data["nvidia_api_key"] = nv_key_input.strip()
            if serp_key_input.strip():
                update_data["serpapi_api_key"] = serp_key_input.strip()
            if gem_key_input.strip():
                update_data["gemini_api_key"] = gem_key_input.strip()
            if update_system_config(api_url, update_data):
                st.success("API credentials updated successfully!")
                st.rerun()
            else:
                st.error("Failed to update credentials.")

    st.divider()

    # Integrations status indicators
    st.markdown("#### 🔌 Service Links")
    if stats:
        integ = stats.get("integrations", {})
        c_nv = "🟢" if integ.get("nvidia_configured") else "🟡"
        c_lens = "🟢" if integ.get("serpapi_configured") else "🟡"
        c_gem = "🟢" if integ.get("gemini_configured") else "🟡"
        c_lar = "🟢" if integ.get("laravel_configured") else "🟡"

        st.markdown(f"{c_nv} **NVIDIA Nemotron NIM**")
        st.markdown(f"{c_lens} **SerpApi (Google Lens)**")
        st.markdown(f"{c_gem} **Gemini / Antigravity AI**")
        st.markdown(f"{c_lar} **Live Laravel Webhook**")
    else:
        st.caption("Connect backend to view active integrations.")

    st.divider()
    if st.button("🔄 Refresh System State", use_container_width=True):
        st.rerun()

# ==============================================================================
# Header Banner
# ==============================================================================
st.markdown(
    """
    <div class="glass-header">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <h1 style="margin: 0; font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #FFFFFF, #CBD5E1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    Newsroom Curation Engine
                </h1>
                <p style="margin: 6px 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                    Bypass scrapers, extract multimodal video evidence, cross-reference real-world location via Google Lens, and generate localized news for human editorial approval.
                </p>
            </div>
            <div style="display: flex; gap: 10px;">
                <span class="badge badge-pending">Strict Laravel Isolation</span>
                <span class="badge badge-published">Gemini 1.5 Pro</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# Main Workspace Tabs
# ==============================================================================
tab_live, tab_review, tab_archive, tab_diag = st.tabs([
    "⚡ Live Pipeline & Ingestion",
    "✍️ Editorial Desk & Approval",
    "📚 Published Articles",
    "⚙️ System Diagnostics",
])

# ==============================================================================
# TAB 1: Live Pipeline & Ingestion Monitor
# ==============================================================================
with tab_live:
    st.markdown("### 📥 Ingest Social Video Link")
    st.write("Submit a social video link from Instagram Reels, TikTok, or X (Twitter) to monitor the end-to-end curation pipeline live.")

    # Quick demo presets
    st.markdown("##### Quick Test Samples:")
    col_p1, col_p2, col_p3 = st.columns(3)
    preset_url = None
    with col_p1:
        if st.button("📸 Instagram Reel (Protest Demo)", use_container_width=True):
            preset_url = "https://www.instagram.com/reel/C8xyz_howrah_protest/"
    with col_p2:
        if st.button("🎵 TikTok Video (Civic Update)", use_container_width=True):
            preset_url = "https://www.tiktok.com/@localupdates/video/73849128372"
    with col_p3:
        if st.button("🐦 X / Twitter Clip (Weather Alert)", use_container_width=True):
            preset_url = "https://x.com/cityweather/status/1805912489012"

    url_input_val = preset_url if preset_url else ""

    col_inp, col_mode, col_llm, col_act = st.columns([4, 3, 3, 2], gap="small")
    with col_inp:
        video_url = st.text_input(
            "Video URL",
            value=url_input_val,
            placeholder="Paste URL (e.g. https://www.instagram.com/reel/...)",
            label_visibility="collapsed",
        )
    with col_mode:
        mode_choice = st.selectbox(
            "Curation Mode",
            options=["🚀 Fully Autonomous (Live DB)", "✍️ Editorial Review (Draft)"],
            index=0,
            label_visibility="collapsed",
        )
    with col_llm:
        cur_def = (sys_config.get("default_llm_provider") or "nvidia_nemotron") if sys_config else "nvidia_nemotron"
        prov_init_idx = 0 if cur_def == "nvidia_nemotron" else 1
        llm_choice = st.selectbox(
            "AI Engine",
            options=["🤖 NVIDIA Nemotron", "🧠 Gemini 1.5 Pro"],
            index=prov_init_idx,
            label_visibility="collapsed",
        )
    with col_act:
        launch_btn = st.button("⚡ Run AI Pipeline", type="primary", use_container_width=True)

    if launch_btn:
        if not video_url or not video_url.startswith("http"):
            st.error("Please enter a valid HTTP/HTTPS social media link.")
        else:
            is_auto = mode_choice.startswith("🚀")
            chosen_prov = "nvidia_nemotron" if "NVIDIA" in llm_choice else "gemini"
            task_id = trigger_curation(api_url, video_url, auto_publish=is_auto, llm_provider=chosen_prov)
            if task_id:
                st.session_state.active_task_id = task_id
                st.session_state.task_logs = [
                    f"[{datetime.now().strftime('%H:%M:%S')}] Task dispatched with ID: {task_id}",
                    f"[{datetime.now().strftime('%H:%M:%S')}] Mode: {'AUTONOMOUS (Live DB Publish)' if is_auto else 'HUMAN-REVIEW (Editorial Draft)'}",
                    f"[{datetime.now().strftime('%H:%M:%S')}] AI Engine: {'NVIDIA Nemotron-3-Ultra-550B' if chosen_prov == 'nvidia_nemotron' else 'Google Gemini 1.5 Pro'}",
                    f"[{datetime.now().strftime('%H:%M:%S')}] Target Source: {video_url}",
                ]
                st.rerun()

    # Active Task Live Monitoring Section
    if st.session_state.active_task_id:
        curr_task_id = st.session_state.active_task_id
        st.divider()
        st.markdown(f"### 🎬 Live Pipeline Monitor &nbsp; <code style='font-size: 0.9rem;'>{curr_task_id}</code>", unsafe_allow_html=True)

        progress_bar = st.empty()
        status_banner = st.empty()
        col_stages, col_terminal = st.columns([1, 1], gap="large")

        stages_container = col_stages.empty()
        terminal_container = col_terminal.empty()

        # Polling Loop
        is_done = False
        iteration = 0

        while not is_done and iteration < 60:
            iteration += 1
            task_info = poll_task_status(api_url, curr_task_id)

            if not task_info:
                status_banner.warning("Waiting for Celery worker heartbeat...")
                time.sleep(1.5)
                continue

            state = task_info.get("state")
            stage = task_info.get("stage") or "INITIALIZING"
            prog = task_info.get("progress", 0)
            details = task_info.get("details", "")

            # Update progress bar
            progress_bar.progress(prog / 100.0, text=f"{details} ({prog}%)")

            # Add to log if new
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_line = f"[{timestamp}] [{stage}] {details}"
            if not st.session_state.task_logs or st.session_state.task_logs[-1] != log_line:
                st.session_state.task_logs.append(log_line)

            # Render Pipeline Stepper Cards
            def get_step_class(step_name: str, target_stage: str, current_prog: int, step_min_prog: int):
                if current_prog >= step_min_prog + 20:
                    return "pipeline-step step-done", "✅"
                elif target_stage == step_name:
                    return "pipeline-step step-active", "🔄"
                else:
                    return "pipeline-step", "⚪"

            # Check execution mode from task metadata
            task_mode = task_info.get("mode", "")
            is_autonomous = "AUTONOMOUS" in task_mode or stage in ("AI_CURATING", "SAVING_AUDIT_DRAFT", "PUBLISHING", "PUBLISHED")

            s1_cls, s1_ico = get_step_class("DOWNLOADING", stage, prog, 15)
            s2_cls, s2_ico = get_step_class("EXTRACTING_MEDIA", stage, prog, 35)
            s3_cls, s3_ico = get_step_class("SEARCHING_CONTEXT", stage, prog, 55)

            task_prov = task_info.get("provider", "") or (sys_config.get("default_llm_provider") if sys_config else "nvidia_nemotron")
            prov_title = "NVIDIA Nemotron" if "nvidia" in task_prov or "nemotron" in task_prov else "Gemini 1.5 Pro"

            if is_autonomous:
                s4_cls, s4_ico = get_step_class("AI_CURATING", stage, prog, 70)
                s5_cls, s5_ico = get_step_class("PUBLISHING", stage, prog, 85)
                s4_label = f"<strong>4. AI Curation ({prov_title}):</strong> Structured schema hydration & entity synthesis"
                s5_label = "<strong>5. Autonomous Publishing:</strong> Laravel MySQL API insertion & alerts"
                mode_badge = f"<span class='badge badge-published' style='margin-left: 8px;'>AUTONOMOUS • {prov_title.split()[0]}</span>"
            else:
                s4_cls, s4_ico = get_step_class("GENERATING_ARTICLE", stage, prog, 75)
                s5_cls, s5_ico = get_step_class("SAVING_DRAFT", stage, prog, 90)
                s4_label = f"<strong>4. AI Generation ({prov_title}):</strong> Multimodal localized draft synthesis"
                s5_label = "<strong>5. Database Persistence:</strong> SQLite review queue storage"
                mode_badge = f"<span class='badge badge-pending' style='margin-left: 8px;'>HUMAN-REVIEW • {prov_title.split()[0]}</span>"

            stages_html = f"""
            <div class="glass-card" style="padding: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                    <h4 style="margin: 0;">Pipeline Stages</h4>
                    {mode_badge}
                </div>
                <div class="{s1_cls}">
                    <span style="font-size: 1.2rem; margin-right: 12px;">{s1_ico}</span>
                    <div><strong>1. Stream Acquisition:</strong> yt-dlp video bypass</div>
                </div>
                <div class="{s2_cls}">
                    <span style="font-size: 1.2rem; margin-right: 12px;">{s2_ico}</span>
                    <div><strong>2. Media Slicing:</strong> ffmpeg MP3 & keyframe extraction</div>
                </div>
                <div class="{s3_cls}">
                    <span style="font-size: 1.2rem; margin-right: 12px;">{s3_ico}</span>
                    <div><strong>3. Context Gathering:</strong> SerpApi Google Lens reverse search</div>
                </div>
                <div class="{s4_cls}">
                    <span style="font-size: 1.2rem; margin-right: 12px;">{s4_ico}</span>
                    <div>{s4_label}</div>
                </div>
                <div class="{s5_cls}">
                    <span style="font-size: 1.2rem; margin-right: 12px;">{s5_ico}</span>
                    <div>{s5_label}</div>
                </div>
            </div>
            """
            stages_container.markdown(stages_html, unsafe_allow_html=True)

            # Render Terminal Output Box
            terminal_lines = "".join([f"<div class='terminal-line'>{line}</div>" for line in st.session_state.task_logs[-10:]])
            terminal_html = f"""
            <div class="glass-card" style="padding: 16px;">
                <h4 style="margin-top: 0; margin-bottom: 14px;">Live Worker Stream</h4>
                <div class="terminal-box">
                    {terminal_lines}
                </div>
            </div>
            """
            terminal_container.markdown(terminal_html, unsafe_allow_html=True)

            # Completion conditions
            if state == "SUCCESS":
                is_done = True
                result_payload = task_info.get("result", {})
                draft_id = result_payload.get("draft_id")
                st.session_state.last_created_draft_id = draft_id
                st.session_state.selected_draft_id = draft_id
                res_mode = result_payload.get("mode", "")

                if res_mode == "AUTONOMOUS":
                    pub_res = result_payload.get("publish_result", {})
                    news_id = pub_res.get("news_id", "LIVE")
                    status_banner.success(
                        f"🚀 **Published Autonomously to Production!** News ID: **#{news_id}** | Headline: _{result_payload.get('headline')}_"
                    )
                    st.info(
                        f"**Category:** {result_payload.get('category')} &nbsp;|&nbsp; **Location:** {result_payload.get('location')} &nbsp;|&nbsp; **Urgency:** {result_payload.get('urgency')} &nbsp;|&nbsp; **Audit Draft:** #{draft_id}"
                    )
                else:
                    status_banner.success(
                        f"🎉 **Curation Complete!** Created Draft **#{draft_id}**: _{result_payload.get('headline')}_"
                    )

                col_btn_rev, _ = st.columns([2, 3])
                with col_btn_rev:
                    target_label = "👉 Open in Editorial Review Desk" if res_mode != "AUTONOMOUS" else "👉 View Audit Record"
                    if st.button(target_label, type="primary", use_container_width=True):
                        st.session_state.active_task_id = None
                        st.rerun()

            elif state == "FAILURE":
                is_done = True
                status_banner.error(f"❌ **Pipeline Failed:** {task_info.get('error')}")

            time.sleep(1.5)

# ==============================================================================
# TAB 2: Human Editorial Desk & Approval Panel
# ==============================================================================
with tab_review:
    st.markdown("### ✍️ Human Editorial Review & Approval Panel")
    st.write("Inspect multimodal keyframes, verify AI-detected location evidence, refine content, and push approved drafts to Laravel.")

    # Draft Filtering & Selection Toolbar
    col_flt, col_srch, col_rel = st.columns([3, 4, 1])
    with col_flt:
        status_filter = st.selectbox(
            "Filter by Status",
            ["PENDING", "ALL", "PUBLISHED", "REJECTED", "FAILED"],
            index=0,
        )
    with col_srch:
        search_query = st.text_input("Search Headlines / Location", placeholder="Filter drafts...")
    with col_rel:
        st.write("")
        st.write("")
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    # Load drafts
    all_drafts = fetch_drafts(api_url, status=status_filter)

    # Filter by search
    if search_query:
        q = search_query.lower()
        all_drafts = [
            d for d in all_drafts
            if q in (d.get("headline") or "").lower()
            or q in (d.get("location") or "").lower()
            or q in (d.get("source_url") or "").lower()
        ]

    if not all_drafts:
        st.info("No drafts found matching the selected filter criteria. Run the curation pipeline in Tab 1 to generate drafts!")
    else:
        # Build selection dict
        draft_options = {
            f"#{d['id']} | {d.get('headline') or 'Untitled'} [{d['status']}]": d['id']
            for d in all_drafts
        }

        # Auto-select last created draft if available
        default_index = 0
        if st.session_state.selected_draft_id:
            for idx, (label, d_id) in enumerate(draft_options.items()):
                if d_id == st.session_state.selected_draft_id:
                    default_index = idx
                    break

        selected_label = st.selectbox("Select Draft to Review", list(draft_options.keys()), index=default_index)
        selected_draft_id = draft_options[selected_label]
        st.session_state.selected_draft_id = selected_draft_id

        # Fetch full draft details
        draft = fetch_draft_detail(api_url, selected_draft_id)

        if draft:
            st.divider()

            # Split Screen Editor Workspace: Left Evidence, Right Editorial
            col_evidence, col_editor = st.columns([1, 1], gap="large")

            # ------------------------------------------------------------------
            # LEFT: Ground-Truth Verification & Media Evidence
            # ------------------------------------------------------------------
            with col_evidence:
                st.markdown("#### 📸 Ground-Truth & Media Evidence")

                # Source Card
                st.markdown(
                    f"""
                    <div class="glass-card" style="padding: 14px;">
                        <span style="font-size: 0.8rem; color: #94A3B8; text-transform: uppercase;">Source Video Link</span><br>
                        <a href="{draft['source_url']}" target="_blank" style="color: #60A5FA; word-break: break-all; font-weight: 500;">
                            {draft['source_url']} ↗
                        </a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Confidence Gauge & Status Badges
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    badge_cls = f"badge-{draft['status'].lower()}"
                    st.markdown(f"Status: <span class='badge {badge_cls}'>{draft['status']}</span>", unsafe_allow_html=True)
                with col_b2:
                    score = draft.get("confidence_score") or 0.0
                    score_pct = int(score * 100)
                    score_color = "#10B981" if score >= 0.85 else ("#F59E0B" if score >= 0.7 else "#EF4444")
                    st.markdown(
                        f"""
                        <div style="text-align: right;">
                            <span style="font-size: 0.85rem; color: #94A3B8;">AI Certainty: </span>
                            <strong style="color: {score_color}; font-size: 1.1rem;">{score_pct}%</strong>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.progress(score, text=None)

                # Extracted Keyframes Gallery
                media_meta = draft.get("media_paths") or {}
                keyframes = media_meta.get("keyframes", [])
                audio_file = media_meta.get("audio_path")
                video_file = media_meta.get("video_path")

                if keyframes:
                    st.markdown("##### Sliced Keyframe Evidence")
                    cols = st.columns(len(keyframes))
                    for i, frame_path in enumerate(keyframes):
                        with cols[i]:
                            if os.path.exists(frame_path):
                                st.image(frame_path, caption=f"Keyframe {i+1}", use_column_width=True)
                            else:
                                st.caption(f"Frame {i+1}: `{os.path.basename(frame_path)}`")

                # Audio Player if available
                if audio_file and os.path.exists(audio_file):
                    st.markdown("##### Extracted Audio Track")
                    st.audio(audio_file)

                # Google Lens & AI Notes
                st.markdown("##### 🔍 Context & Geolocation Analysis")
                st.markdown(
                    f"""
                    <div class="glass-card">
                        <div style="margin-bottom: 8px;">
                            <span style="color: #94A3B8; font-size: 0.85rem;">Detected Location:</span><br>
                            <strong style="color: #38BDF8; font-size: 1.1rem;">📍 {draft.get('location') or 'Unspecified'}</strong>
                        </div>
                        <div>
                            <span style="color: #94A3B8; font-size: 0.85rem;">AI Fact-Checking Notes:</span><br>
                            <p style="margin: 4px 0 0 0; color: #CBD5E1; font-size: 0.9rem; line-height: 1.5;">
                                {draft.get('ai_notes') or 'No contextual notes recorded.'}
                            </p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if draft.get("laravel_post_id"):
                    st.success(f"✅ Published to Live Laravel App (Post ID: `{draft['laravel_post_id']}`)")

            # ------------------------------------------------------------------
            # RIGHT: Editorial Studio & WYSIWYG Article Editor
            # ------------------------------------------------------------------
            with col_editor:
                st.markdown("#### 📰 Editorial Article Studio")

                # Category selector (matching CodeCanyon template categories)
                cat_col, loc_col = st.columns(2)
                with cat_col:
                    category_choice = st.selectbox(
                        "Target Category",
                        ["1 - Local News", "2 - Breaking News", "3 - Politics", "4 - Civic / Infrastructure", "5 - Sports", "6 - Weather Alert"],
                        index=0,
                    )
                    category_id = int(category_choice.split(" - ")[0])
                with loc_col:
                    edit_location = st.text_input("Article Geotag / Location", value=draft.get("location") or "")

                # Headline
                edit_headline = st.text_input("Headline", value=draft.get("headline") or "")
                st.caption(f"Characters: {len(edit_headline)} | Recommended: 60-90 characters")

                # Summary
                edit_summary = st.text_area("Lead / Executive Summary", value=draft.get("summary") or "", height=85)

                # Tags
                tags_list = draft.get("tags") or []
                edit_tags_str = st.text_input("Tags (comma separated)", value=", ".join(tags_list))

                # Body Content Tabs: Editor vs Live Preview
                tab_body_edit, tab_body_prev = st.tabs(["💻 HTML Source Editor", "👁️ Live Reader Preview"])

                with tab_body_edit:
                    edit_body = st.text_area(
                        "HTML Body Content",
                        value=draft.get("body_content") or "",
                        height=260,
                        help="Semantic HTML supported: <p>, <strong>, <em>, <ul>, <li>, <blockquote>",
                    )

                with tab_body_prev:
                    st.markdown(
                        f"""
                        <div class="article-preview">
                            <span style="color: #6366F1; font-weight: 700; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em;">
                                {category_choice.split(' - ')[1]} • 📍 {edit_location}
                            </span>
                            <h1>{edit_headline}</h1>
                            <div class="meta-bar">
                                Curated on {datetime.now().strftime('%B %d, %Y')} • Verified via Visual Geolocation
                            </div>
                            <div class="summary-box">
                                {edit_summary}
                            </div>
                            <div class="body-text">
                                {edit_body}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                # Action Bar
                st.markdown("<br>", unsafe_allow_html=True)
                btn_col1, btn_col2, btn_col3 = st.columns([1, 1.5, 1], gap="small")

                with btn_col1:
                    if st.button("💾 Save Edits", use_container_width=True):
                        update_payload = {
                            "headline": edit_headline,
                            "summary": edit_summary,
                            "location": edit_location,
                            "tags": [t.strip() for t in edit_tags_str.split(",") if t.strip()],
                            "body_content": edit_body,
                        }
                        res = requests.patch(f"{api_url}/api/v1/drafts/{selected_draft_id}", json=update_payload)
                        if res.status_code == 200:
                            st.success("Draft updated!")
                            time.sleep(0.8)
                            st.rerun()
                        else:
                            st.error(f"Save failed: {res.text}")

                with btn_col2:
                    is_published = draft["status"] == "PUBLISHED"
                    btn_label = "✅ Published" if is_published else "🚀 Approve & Push to Laravel"
                    if st.button(btn_label, type="primary", disabled=is_published, use_container_width=True):
                        with st.spinner("Pushing article to live Laravel news app via REST API..."):
                            res = requests.post(f"{api_url}/api/v1/drafts/{selected_draft_id}/publish?category_id={category_id}")
                        if res.status_code == 200:
                            pub_info = res.json()
                            st.balloons()
                            st.success(f"Article live on Laravel! Post ID: {pub_info.get('laravel_post_id')}")
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error(f"Publish failed: {res.text}")

                with btn_col3:
                    is_rejected = draft["status"] in ["REJECTED", "PUBLISHED"]
                    if st.button("❌ Reject", disabled=is_rejected, use_container_width=True):
                        res = requests.post(f"{api_url}/api/v1/drafts/{selected_draft_id}/reject")
                        if res.status_code == 200:
                            st.warning("Draft rejected. Media cleaned up.")
                            time.sleep(0.8)
                            st.rerun()
                        else:
                            st.error(f"Rejection failed: {res.text}")

# ==============================================================================
# TAB 3: Published Articles & History
# ==============================================================================
with tab_archive:
    st.markdown("### 📚 Published Articles Archive")
    st.write("Record of all news articles successfully reviewed and pushed to the live Flutter/Laravel production platform.")

    published_drafts = fetch_drafts(api_url, status="PUBLISHED")

    if not published_drafts:
        st.info("No articles published yet. When you approve a draft in the Editorial Desk, it will appear here with its Laravel reference ID.")
    else:
        for p in published_drafts:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="badge badge-published">Published Live</span>
                            <span style="color: #94A3B8; font-size: 0.85rem; margin-left: 10px;">Post ID: <code>{p.get('laravel_post_id') or 'N/A'}</code></span>
                            <h3 style="margin: 8px 0 4px 0; color: #F8FAFC;">{p.get('headline')}</h3>
                            <p style="margin: 0 0 10px 0; color: #94A3B8; font-size: 0.9rem;">📍 {p.get('location') or 'Local'} • Source: <a href="{p.get('source_url')}" target="_blank" style="color: #60A5FA;">{p.get('source_url')}</a></p>
                        </div>
                        <div>
                            <span style="font-size: 0.85rem; color: #10B981; font-weight: 700;">{int((p.get('confidence_score') or 0)*100)}% Confidence</span>
                        </div>
                    </div>
                    <div style="background: rgba(0,0,0,0.25); border-radius: 8px; padding: 12px; margin-top: 10px; color: #CBD5E1; font-size: 0.9rem;">
                        {p.get('summary')}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ==============================================================================
# TAB 4: System Diagnostics & Maintenance
# ==============================================================================
with tab_diag:
    st.markdown("### ⚙️ System Diagnostics & Cache Maintenance")
    st.write("Monitor service connectivity, inspect database records, and manage temporary media disk utilization.")

    col_d1, col_d2 = st.columns(2, gap="large")

    with col_d1:
        st.markdown("#### 🏥 Service Health")
        diag_stats = fetch_system_stats(api_url)
        if diag_stats:
            st.json(diag_stats)
        else:
            st.error("Could not fetch system stats from backend.")

    with col_d2:
        st.markdown("#### 🧹 Disk & Temporary Media Cache")
        st.write("Per project specifications, temporary downloaded media files (.mp4, .mp3, keyframes) should be pruned after publication or rejection to prevent disk bloat.")

        if diag_stats:
            storage = diag_stats.get("storage", {})
            st.metric("Cached Media Files", f"{storage.get('file_count', 0)} files")
            st.metric("Disk Storage Consumed", f"{storage.get('size_mb', 0)} MB")

        if st.button("🧹 Purge Orphaned Temp Media Cache", type="secondary"):
            try:
                clean_res = requests.post(f"{api_url}/api/v1/system/cleanup", timeout=5)
                if clean_res.status_code == 200:
                    clean_data = clean_res.json()
                    st.success(f"Purged {clean_data.get('deleted_files')} files ({clean_data.get('freed_mb')} MB freed)!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Cleanup failed: {clean_res.text}")
            except Exception as e:
                st.error(f"Cleanup error: {e}")
