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
# 3-Tone Design System
# Tone 1  (BG):     #1B2030  — soft navy background
# Tone 2  (ACCENT): #7B8AF2  — soft periwinkle / muted blue-violet
# Tone 3  (TEXT):   #E8ECF4  — near-white warm gray for max readability
#
# Derived shades only from those 3:
#   bg-lighter:   #242B3E   — card surfaces
#   bg-lightest:  #2E3650   — inputs, hover states
#   accent-dim:   rgba(123,138,242,0.15)  — tinted backgrounds
#   accent-med:   rgba(123,138,242,0.35)  — borders, highlights
#   text-dim:     #9BA3B8   — secondary / muted text (still WCAG AA on #1B2030)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg:         #1B2030;
        --bg-card:    #242B3E;
        --bg-input:   #2E3650;
        --accent:     #7B8AF2;
        --accent-dim: rgba(123,138,242,0.15);
        --accent-med: rgba(123,138,242,0.35);
        --text:       #E8ECF4;
        --text-dim:   #9BA3B8;
        --radius:     12px;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text);
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        letter-spacing: -0.02em;
        color: var(--text);
    }
    p, span, div, label, li, td, th, a {
        color: var(--text);
    }

    /* ===== App Background ===== */
    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] > div {
        background: #171C2C;
    }

    /* ===== Cards ===== */
    .glass-card {
        background: var(--bg-card);
        border: 1px solid rgba(123,138,242,0.12);
        border-radius: var(--radius);
        padding: 22px;
        margin-bottom: 14px;
    }

    .glass-header {
        background: var(--bg-card);
        border: 1px solid var(--accent-med);
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
    }

    /* ===== Badges — only accent + opacity variations ===== */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        white-space: nowrap;
        color: var(--text);
    }
    .badge-pending    { background: var(--accent-dim); border: 1px solid var(--accent-med); color: var(--accent); }
    .badge-published  { background: var(--accent-dim); border: 1px solid var(--accent-med); color: var(--text); }
    .badge-approved   { background: var(--accent-dim); border: 1px solid var(--accent-med); color: var(--text); }
    .badge-rejected   { background: rgba(123,138,242,0.08); border: 1px solid rgba(123,138,242,0.2); color: var(--text-dim); }
    .badge-failed     { background: rgba(123,138,242,0.08); border: 1px solid rgba(123,138,242,0.2); color: var(--text-dim); }
    .badge-processing { background: var(--accent-dim); border: 1px solid var(--accent-med); color: var(--accent); }
    .badge-queued     { background: var(--accent-dim); border: 1px solid var(--accent-med); color: var(--accent); }

    /* ===== Pipeline Steps ===== */
    .step-row {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 14px 18px;
        border-radius: var(--radius);
        margin-bottom: 8px;
        background: var(--bg-card);
        border: 1px solid rgba(123,138,242,0.1);
    }
    .step-active {
        background: var(--accent-dim);
        border-color: var(--accent-med);
    }
    .step-done {
        background: rgba(123,138,242,0.06);
        border-color: rgba(123,138,242,0.2);
    }
    .step-icon {
        font-size: 1.3rem;
        flex-shrink: 0;
        width: 32px;
        text-align: center;
    }
    .step-label {
        font-size: 0.9rem;
        line-height: 1.4;
        color: var(--text);
    }
    .step-label strong { color: var(--text); }

    /* ===== Terminal ===== */
    .terminal-box {
        background: #151A28;
        border: 1px solid rgba(123,138,242,0.15);
        border-radius: var(--radius);
        padding: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: var(--accent);
        max-height: 280px;
        overflow-y: auto;
        line-height: 1.6;
    }
    .terminal-line { margin: 3px 0; }

    /* ===== Article Preview (Light mode preview) ===== */
    .article-preview {
        background: #FFFFFF;
        color: #1B2030;
        padding: 32px;
        border-radius: var(--radius);
    }
    .article-preview h1 {
        font-family: 'Outfit', sans-serif;
        color: #1B2030;
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1.25;
        margin-bottom: 12px;
    }
    .article-preview .meta-bar {
        font-size: 0.85rem;
        color: #6B7280;
        margin-bottom: 20px;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 12px;
    }
    .article-preview .summary-box {
        background: #F3F4F6;
        border-left: 4px solid var(--accent);
        padding: 14px 18px;
        margin-bottom: 24px;
        font-style: italic;
        color: #374151;
    }
    .article-preview .body-text {
        font-size: 1.02rem;
        line-height: 1.7;
        color: #1F2937;
    }

    /* ===== Stat Card ===== */
    .stat-card {
        background: var(--bg-card);
        border: 1px solid rgba(123,138,242,0.12);
        border-radius: var(--radius);
        padding: 20px;
        text-align: center;
    }
    .stat-number {
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: var(--accent);
    }
    .stat-label {
        font-size: 0.8rem;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 4px;
    }

    /* ===== Streamlit overrides ===== */
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: var(--text);
    }
    div[data-testid="stMetricLabel"] {
        color: var(--text-dim) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--bg-card);
        border-radius: var(--radius) var(--radius) 0 0;
        padding: 6px 6px 0;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        font-weight: 600;
        font-size: 0.88rem;
        color: var(--text-dim);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        font-weight: 700;
        color: var(--text);
    }
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
    "queue_tasks": [],
    "monitoring_task": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

API_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://127.0.0.1:8000")

# ==============================================================================
# Helper Functions
# ==============================================================================

def detect_source(url: str) -> str:
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
# Sidebar
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 14px; margin-bottom: 6px;">
            <div style="width: 40px; height: 40px; border-radius: 10px; background: var(--accent); display: flex; align-items: center; justify-content: center; font-size: 1.3rem;">⚡</div>
            <div>
                <h2 style="margin: 0; font-size: 1.35rem; font-weight: 800;">FOCUS</h2>
                <span style="font-size: 0.7rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.1em;">AI News Command Center</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    api_url = st.text_input("Backend URL", value=API_BASE_URL, help="FastAPI server address")

    stats = fetch_system_stats(api_url)
    if stats:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:8px;margin:8px 0;"><div style="width:8px;height:8px;border-radius:50%;background:var(--accent);"></div><span style="font-size:0.85rem;font-weight:600;color:var(--text);">Pipeline Online</span></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="display:flex;align-items:center;gap:8px;margin:8px 0;"><div style="width:8px;height:8px;border-radius:50%;background:var(--text-dim);"></div><span style="font-size:0.85rem;font-weight:600;color:var(--text-dim);">Backend Offline</span></div>',
            unsafe_allow_html=True,
        )

    st.divider()

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

    # AI Model Switcher
    st.markdown("##### AI Engine")
    sys_config = fetch_system_config(api_url)
    current_prov = (sys_config.get("default_llm_provider") or "nvidia_nemotron") if sys_config else "nvidia_nemotron"
    prov_idx = 0 if current_prov == "nvidia_nemotron" else 1

    chosen_model = st.radio(
        "Select Model", ["NVIDIA Nemotron", "Gemini 1.5 Pro"],
        index=prov_idx, label_visibility="collapsed",
    )
    active_prov = "nvidia_nemotron" if "NVIDIA" in chosen_model else "gemini"

    if sys_config and active_prov != sys_config.get("default_llm_provider"):
        if st.button("Apply as Default", use_container_width=True, type="primary"):
            if update_system_config(api_url, {"default_llm_provider": active_prov}):
                st.toast(f"Switched to {chosen_model}!")
                st.rerun()

    with st.expander("API Credentials", expanded=False):
        st.caption("[NVIDIA key](https://build.nvidia.com/nvidia/nemotron-3-ultra-550b-a55b) · [SerpApi](https://serpapi.com/manage-api-key) · [Gemini](https://aistudio.google.com/)")
        nv_k = st.text_input("NVIDIA Key", type="password", placeholder="nvapi-...")
        serp_k = st.text_input("SerpApi Key", type="password", placeholder="Enter key...")
        gem_k = st.text_input("Gemini Key", type="password", placeholder="Enter key...")
        if st.button("Save Keys", use_container_width=True):
            upd = {"default_llm_provider": active_prov}
            if nv_k.strip(): upd["nvidia_api_key"] = nv_k.strip()
            if serp_k.strip(): upd["serpapi_api_key"] = serp_k.strip()
            if gem_k.strip(): upd["gemini_api_key"] = gem_k.strip()
            if update_system_config(api_url, upd):
                st.success("Saved!")
                st.rerun()

    st.divider()

    if stats:
        integ = stats.get("integrations", {})
        services = [
            ("NVIDIA NIM", integ.get("nvidia_configured")),
            ("SerpApi Lens", integ.get("serpapi_configured")),
            ("Gemini AI", integ.get("gemini_configured")),
            ("Laravel API", integ.get("laravel_configured")),
        ]
        for name, ok in services:
            dot_color = "var(--accent)" if ok else "var(--bg-input)"
            st.markdown(f"<span style='font-size:0.85rem;color:var(--text);'><span style='color:{dot_color};'>●</span> {name}</span>", unsafe_allow_html=True)

    st.divider()
    if st.button("Refresh", use_container_width=True):
        st.rerun()




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
    st.markdown("### Submit Video Links")
    st.markdown("Paste any video URL from **YouTube**, **Instagram**, **TikTok**, **X/Twitter**, **Facebook**, **Reddit**, or any web source.")

    # Supported platforms — single tone badges
    platforms = ["YouTube", "Instagram", "TikTok", "X / Twitter", "Facebook", "Reddit", "Any URL"]
    badge_html = " ".join([f"<span class='badge badge-queued'>{p}</span>" for p in platforms])
    st.markdown(f'<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px;">{badge_html}</div>', unsafe_allow_html=True)

    # Input
    col_url, col_mode, col_go = st.columns([5, 3, 2], gap="small")
    with col_url:
        video_url = st.text_input("Video URL", placeholder="https://www.youtube.com/watch?v=... or any video link", label_visibility="collapsed", key="submit_url")
    with col_mode:
        mode_choice = st.selectbox("Mode", ["Autonomous (Live Publish)", "Editorial Review (Draft)"], index=0, label_visibility="collapsed", key="submit_mode")
    with col_go:
        submit_btn = st.button("⚡ Queue & Run", type="primary", use_container_width=True, key="submit_btn")

    # Multi-URL
    with st.expander("Paste Multiple URLs (one per line)", expanded=False):
        multi_urls = st.text_area(
            "URLs", height=120,
            placeholder="https://www.youtube.com/watch?v=abc123\nhttps://www.instagram.com/reel/xyz/\nhttps://www.tiktok.com/@user/video/123",
            label_visibility="collapsed", key="multi_urls",
        )
        multi_submit = st.button("Queue All URLs", use_container_width=True, key="multi_submit_btn")

    # Single submit
    if submit_btn and video_url:
        if not video_url.startswith("http"):
            st.error("Please enter a valid URL starting with http:// or https://")
        else:
            is_auto = "Autonomous" in mode_choice
            resp = trigger_curation(api_url, video_url, auto_publish=is_auto, llm_provider=active_prov)
            if resp:
                src = detect_source(video_url)
                st.session_state.queue_tasks.append({
                    "url": video_url, "task_id": resp["task_id"],
                    "mode": resp.get("mode", "UNKNOWN"), "provider": active_prov,
                    "status": "QUEUED", "source": src,
                    "submitted_at": datetime.now().strftime("%H:%M:%S"),
                })
                st.session_state.active_task_id = resp["task_id"]
                st.toast(f"Queued: {source_label(src)} link submitted!")
                st.rerun()

    # Multi submit
    if multi_submit and multi_urls:
        url_list = [u.strip() for u in multi_urls.strip().split("\n") if u.strip()]
        if url_list:
            is_auto = "Autonomous" in mode_choice
            batch_resp = trigger_batch(api_url, url_list, auto_publish=is_auto, llm_provider=active_prov)
            if batch_resp:
                for task_resp in batch_resp.get("tasks", []):
                    src = detect_source(task_resp["source_url"])
                    st.session_state.queue_tasks.append({
                        "url": task_resp["source_url"], "task_id": task_resp["task_id"],
                        "mode": task_resp.get("mode", "UNKNOWN"), "provider": active_prov,
                        "status": "QUEUED", "source": src,
                        "submitted_at": datetime.now().strftime("%H:%M:%S"),
                    })
                rejected = batch_resp.get("rejected_urls", [])
                st.toast(f"{batch_resp['accepted']} URLs queued" + (f", {len(rejected)} rejected" if rejected else ""))
                st.rerun()

    # Queue display
    st.divider()
    st.markdown("### Submission Queue")

    if not st.session_state.queue_tasks:
        st.info("No links in queue yet. Submit a URL above to get started.")
    else:
        for idx, item in enumerate(reversed(st.session_state.queue_tasks)):
            real_idx = len(st.session_state.queue_tasks) - 1 - idx
            src = item.get("source", "other")
            status_val = item.get("status", "QUEUED")

            cols = st.columns([0.4, 5, 1.2, 1.3, 1, 0.8])
            with cols[0]:
                st.markdown(f"**{real_idx+1}**")
            with cols[1]:
                st.markdown(f"{source_icon(src)} `{item['url'][:80]}{'...' if len(item['url']) > 80 else ''}`")
            with cols[2]:
                st.caption(source_label(src))
            with cols[3]:
                mode_short = "Auto" if "AUTO" in item.get("mode", "") else "Review"
                st.caption(mode_short)
            with cols[4]:
                badge_cls = {"QUEUED": "badge-queued", "PROCESSING": "badge-processing", "COMPLETED": "badge-published", "FAILED": "badge-failed"}.get(status_val, "badge-queued")
                st.markdown(f"<span class='badge {badge_cls}' style='font-size:0.7rem;'>{status_val}</span>", unsafe_allow_html=True)
            with cols[5]:
                if st.button("👁", key=f"monitor_{real_idx}", help="Monitor this job"):
                    st.session_state.active_task_id = item["task_id"]
                    st.session_state.task_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring task: {item['task_id']}"]


# ==============================================================================
# TAB 2: Active Jobs
# ==============================================================================
with tab_jobs:
    st.markdown("### Active Pipeline Jobs")
    st.markdown("Real-time view of running AI curation pipelines. Select a job from the queue to see detailed progress.")

    active_id = st.session_state.active_task_id

    if not active_id:
        if st.session_state.queue_tasks:
            st.markdown("#### Job Status Overview")
            for idx, item in enumerate(reversed(st.session_state.queue_tasks)):
                task_info = poll_task_status(api_url, item["task_id"])
                state = task_info.get("state", "PENDING") if task_info else "UNKNOWN"
                prog = task_info.get("progress", 0) if task_info else 0
                details = task_info.get("details", "") if task_info else ""
                stage = task_info.get("stage", "") if task_info else ""

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
                        if st.button("Monitor", key=f"job_mon_{idx}", use_container_width=True):
                            st.session_state.active_task_id = item["task_id"]
                            st.session_state.task_logs = [f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring: {item['task_id']}"]
                            st.rerun()
                    st.divider()
        else:
            st.info("No active jobs. Submit URLs in the **Submit & Queue** tab.")
    else:
        curr_task_id = active_id
        st.markdown(f"#### Monitoring Job: `{curr_task_id[:16]}...`")

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
                status_banner.warning("Waiting for Celery worker heartbeat...")
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
                s4_lbl = f"<strong>4. AI Curation ({prov_name}):</strong> Schema hydration"
                s5_lbl = "<strong>5. Publishing:</strong> Laravel API insertion"
                mode_badge = "<span class='badge badge-published'>AUTONOMOUS</span>"
            else:
                s4c, s4i = get_step("GENERATING_ARTICLE", stage, prog, 75)
                s5c, s5i = get_step("SAVING_DRAFT", stage, prog, 90)
                s4_lbl = f"<strong>4. AI Draft ({prov_name}):</strong> Multimodal synthesis"
                s5_lbl = "<strong>5. Saving:</strong> SQLite review queue"
                mode_badge = "<span class='badge badge-pending'>EDITORIAL REVIEW</span>"

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

                for qi in st.session_state.queue_tasks:
                    if qi["task_id"] == curr_task_id:
                        qi["status"] = "COMPLETED"

                if res_mode == "AUTONOMOUS":
                    pub_res = result.get("publish_result", {})
                    news_id = pub_res.get("news_id", "LIVE")
                    status_banner.success(f"Published! News ID: #{news_id} — {result.get('headline')}")
                else:
                    status_banner.success(f"Draft Created! #{draft_id}: {result.get('headline')}")

            elif state == "FAILURE":
                is_done = True
                for qi in st.session_state.queue_tasks:
                    if qi["task_id"] == curr_task_id:
                        qi["status"] = "FAILED"
                status_banner.error(f"Failed: {task_info.get('error')}")

            time.sleep(1.5)


# ==============================================================================
# TAB 3: Editorial Desk
# ==============================================================================
with tab_review:
    st.markdown("### Editorial Review & Approval")
    st.markdown("Inspect AI-curated content, verify evidence, edit articles, and push approved drafts to production.")

    col_flt, col_srch, col_rel = st.columns([3, 4, 1])
    with col_flt:
        status_filter = st.selectbox("Filter", ["PENDING", "ALL", "PUBLISHED", "REJECTED", "FAILED"], index=0, key="ed_filter")
    with col_srch:
        search_q = st.text_input("Search", placeholder="Filter by headline or location...", key="ed_search")
    with col_rel:
        st.write("")
        st.write("")
        if st.button("Refresh", use_container_width=True, key="ed_refresh"):
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
                st.markdown("#### Evidence & Media")

                st.markdown(
                    f"""<div class="glass-card" style="padding:16px;">
                        <span style="font-size:0.8rem;color:var(--text-dim);text-transform:uppercase;">Source</span><br>
                        <a href="{draft['source_url']}" target="_blank" style="color:var(--accent);word-break:break-all;font-weight:500;">{draft['source_url']}</a>
                    </div>""",
                    unsafe_allow_html=True,
                )

                c_b1, c_b2 = st.columns(2)
                with c_b1:
                    bcls = f"badge-{draft['status'].lower()}"
                    st.markdown(f"<span class='badge {bcls}'>{draft['status']}</span>", unsafe_allow_html=True)
                with c_b2:
                    score = draft.get("confidence_score") or 0.0
                    st.markdown(f"<div style='text-align:right;'><span style='color:var(--text-dim);font-size:0.85rem;'>AI Confidence: </span><strong style='color:var(--accent);font-size:1.1rem;'>{int(score*100)}%</strong></div>", unsafe_allow_html=True)
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

                st.markdown("##### Context & Location")
                st.markdown(
                    f"""<div class="glass-card">
                        <div style="margin-bottom:8px;">
                            <span style="color:var(--text-dim);font-size:0.85rem;">Location:</span><br>
                            <strong style="color:var(--accent);">📍 {draft.get('location') or 'Unspecified'}</strong>
                        </div>
                        <div>
                            <span style="color:var(--text-dim);font-size:0.85rem;">AI Notes:</span>
                            <p style="margin:4px 0 0;color:var(--text);font-size:0.9rem;line-height:1.5;">{draft.get('ai_notes') or 'No notes.'}</p>
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )

                if draft.get("laravel_post_id"):
                    st.success(f"Live on Laravel (Post ID: `{draft['laravel_post_id']}`)")

            # RIGHT: Editor
            with col_ed:
                st.markdown("#### Article Editor")

                cat_c, loc_c = st.columns(2)
                with cat_c:
                    cat = st.selectbox("Category", [
                        "1 - Local News", "2 - Breaking News", "3 - Politics", "4 - Civic",
                        "5 - Sports", "6 - Weather", "7 - Entertainment", "8 - Technology",
                    ], index=0, key="ed_cat")
                    cat_id = int(cat.split(" - ")[0])
                with loc_c:
                    ed_loc = st.text_input("Location", value=draft.get("location") or "", key="ed_loc")

                ed_head = st.text_input("Headline", value=draft.get("headline") or "", key="ed_head")
                st.caption(f"{len(ed_head)} chars — recommended 60-90")

                ed_sum = st.text_area("Summary", value=draft.get("summary") or "", height=80, key="ed_sum")

                tags_list = draft.get("tags") or []
                ed_tags = st.text_input("Tags (comma-separated)", value=", ".join(tags_list), key="ed_tags")

                tab_edit, tab_prev = st.tabs(["HTML Editor", "Preview"])
                with tab_edit:
                    ed_body = st.text_area("HTML Body", value=draft.get("body_content") or "", height=240, key="ed_body")
                with tab_prev:
                    st.markdown(
                        f"""<div class="article-preview">
                            <span style="color:var(--accent);font-weight:700;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em;">{cat.split(' - ')[1]} · 📍 {ed_loc}</span>
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
                    if st.button("Save", use_container_width=True, key="ed_save"):
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
                    if st.button("Published" if is_pub else "Approve & Publish", type="primary", disabled=is_pub, use_container_width=True, key="ed_pub"):
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
                    if st.button("Reject", disabled=is_rej, use_container_width=True, key="ed_rej"):
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
    st.markdown("### Published Articles")
    st.markdown("All articles pushed to the live production platform.")

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
                                <span style="color:var(--text-dim);font-size:0.85rem;">Post #{p.get('laravel_post_id') or 'N/A'} · {source_icon(src)} {source_label(src)}</span>
                            </div>
                            <h3 style="margin:0 0 6px;font-size:1.1rem;">{p.get('headline')}</h3>
                            <p style="margin:0;color:var(--text-dim);font-size:0.88rem;">📍 {p.get('location') or 'Local'} · <a href="{p.get('source_url')}" target="_blank" style="color:var(--accent);">{p.get('source_url','')[:60]}...</a></p>
                        </div>
                        <div style="text-align:right;flex-shrink:0;">
                            <span style="font-size:0.88rem;color:var(--accent);font-weight:700;">{int((p.get('confidence_score') or 0)*100)}%</span>
                        </div>
                    </div>
                    <div style="background:var(--bg-input);border-radius:8px;padding:12px;margin-top:10px;color:var(--text);font-size:0.9rem;">
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
    st.markdown("### Batch URL Upload")
    st.markdown("Upload a `.txt` or `.csv` file containing one video URL per line. All URLs are queued simultaneously.")

    st.markdown(
        """
        <div class="glass-card" style="padding:20px;">
            <h4 style="margin:0 0 10px;">File Format Guide</h4>
            <div style="font-size:0.9rem;color:var(--text);line-height:1.7;">
                <strong>Text file (.txt):</strong> One URL per line<br>
                <strong>CSV file (.csv):</strong> URL in the first column<br>
                <strong>Comments:</strong> Lines starting with <code>#</code> are ignored<br>
                <strong>Supported:</strong> YouTube, Instagram, TikTok, X/Twitter, Facebook, Reddit, any URL
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_upload, col_opts = st.columns([2, 1])
    with col_upload:
        uploaded_file = st.file_uploader("Upload URL file", type=["txt", "csv"], help="Text or CSV file with one URL per line", key="batch_file")
    with col_opts:
        batch_mode = st.selectbox("Mode", ["Autonomous", "Editorial Review"], key="batch_mode")
        batch_prov = st.selectbox("AI Engine", ["NVIDIA Nemotron", "Gemini 1.5 Pro"], key="batch_prov")

    if uploaded_file:
        file_content = uploaded_file.read()
        try:
            text_preview = file_content.decode("utf-8")
        except UnicodeDecodeError:
            text_preview = file_content.decode("latin-1")

        lines = [l.strip() for l in text_preview.split("\n") if l.strip() and not l.strip().startswith("#")]
        url_count = len(lines)

        st.markdown(f"**Found {url_count} URLs in uploaded file:**")

        with st.expander(f"Preview ({min(url_count, 20)} of {url_count} URLs)", expanded=True):
            for i, line in enumerate(lines[:20]):
                if "," in line:
                    line = line.split(",")[0].strip()
                src = detect_source(line)
                st.markdown(f"`{i+1}.` {source_icon(src)} `{line}`")
            if url_count > 20:
                st.caption(f"...and {url_count - 20} more")

        if st.button("Upload & Queue All", type="primary", use_container_width=True, key="batch_go"):
            is_auto = "Autonomous" in batch_mode
            prov = "nvidia_nemotron" if "NVIDIA" in batch_prov else "gemini"
            result = upload_file_batch(api_url, file_content, uploaded_file.name, is_auto, prov)
            if result:
                for t in result.get("tasks", []):
                    src = detect_source(t["source_url"])
                    st.session_state.queue_tasks.append({
                        "url": t["source_url"], "task_id": t["task_id"],
                        "mode": t.get("mode", "UNKNOWN"), "provider": prov,
                        "status": "QUEUED", "source": src,
                        "submitted_at": datetime.now().strftime("%H:%M:%S"),
                    })
                rejected = result.get("rejected_urls", [])
                st.success(f"{result['accepted']} URLs queued successfully!")
                if rejected:
                    st.warning(f"{len(rejected)} URLs rejected: {', '.join(rejected[:5])}")
                st.rerun()


# ==============================================================================
# TAB 6: System
# ==============================================================================
with tab_diag:
    st.markdown("### System Configuration & Diagnostics")

    diag_stats = fetch_system_stats(api_url)

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
                st.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.divider()

    col_health, col_cache = st.columns(2, gap="large")

    with col_health:
        st.markdown("#### Service Health")
        if diag_stats:
            st.code(json.dumps(diag_stats, indent=2), language="json")
        else:
            st.error("Cannot reach backend.")

    with col_cache:
        st.markdown("#### Cache Management")
        st.markdown("Temporary files accumulate during pipeline runs. Purge them after articles are published.")

        if diag_stats:
            storage = diag_stats.get("storage", {})
            st.metric("Cached Files", f"{storage.get('file_count', 0)} files")
            st.metric("Disk Used", f"{storage.get('size_mb', 0)} MB")

        if st.button("Purge Temp Media", key="diag_clean"):
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
        st.markdown("#### Queue Session Stats")
        q = st.session_state.queue_tasks
        total_q = len(q)
        completed_q = sum(1 for x in q if x.get("status") == "COMPLETED")
        failed_q = sum(1 for x in q if x.get("status") == "FAILED")
        active_q = total_q - completed_q - failed_q

        st.markdown(f"**Total Submitted:** {total_q}")
        st.markdown(f"**Completed:** {completed_q}")
        st.markdown(f"**Active/Queued:** {active_q}")
        st.markdown(f"**Failed:** {failed_q}")

        if st.button("Clear Session Queue", key="clear_queue"):
            st.session_state.queue_tasks = []
            st.session_state.active_task_id = None
            st.toast("Queue cleared!")
            st.rerun()
