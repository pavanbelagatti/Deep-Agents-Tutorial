"""
app.py

Streamlit UI for the Competitive Intelligence Deep Agent.
Run with: streamlit run app.py
"""

import os
import time
import threading
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Competitive Intel Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# Styling
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

  :root {
    --bg:       #0d0f14;
    --surface:  #151820;
    --border:   #252933;
    --accent:   #4f8ef7;
    --accent2:  #1e2d4a;
    --green:    #3ecf8e;
    --yellow:   #f7b731;
    --text:     #e8eaf0;
    --muted:    #6b7280;
  }

  html, body, .stApp { background-color: var(--bg) !important; }

  h1, h2, h3, h4 {
    font-family: 'DM Serif Display', serif !important;
    color: var(--text) !important;
  }
  p, li, span, label, div {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
  }
  code, pre { font-family: 'JetBrains Mono', monospace !important; }

  [data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
  }

  input, textarea {
    background-color: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
  }
  input:focus, textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent2) !important;
  }

  .stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.18s ease !important;
  }
  .stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }
  .stButton > button:disabled { opacity: 0.35 !important; transform: none !important; }

  .stTextInput label, .stTextArea label {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.07em !important;
  }

  .log-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--muted);
    line-height: 1.9;
  }

  .rate-limit-box {
    background: #1a1500;
    border: 1px solid #3d3000;
    border-left: 3px solid var(--yellow);
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    color: var(--yellow);
    line-height: 1.9;
  }

  .report-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
    line-height: 1.8;
  }

  .how-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.2rem;
  }

  #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Intel Agent")
    st.caption("Competitive research powered by Deep Agents")
    st.markdown("---")

    st.markdown("### API Keys")
    st.caption("Stored only for this session — never saved to disk.")

    openai_key = st.text_input(
        "OpenAI API Key",
        value=os.environ.get("OPENAI_API_KEY", ""),
        type="password",
        placeholder="sk-...",
    )
    tavily_key = st.text_input(
        "Tavily API Key",
        value=os.environ.get("TAVILY_API_KEY", ""),
        type="password",
        placeholder="tvly-...",
    )

    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    if tavily_key:
        os.environ["TAVILY_API_KEY"] = tavily_key

    keys_ok = bool(openai_key and tavily_key)

    if keys_ok:
        st.success("✅ Keys set — ready to run")
    else:
        st.warning("⚠️ Both keys are required")

    st.markdown("---")
    st.markdown("### How it works")
    st.markdown("""
A **deep agent** does more than search — it:

**📋 Plans** research as a todo list before starting

**🔀 Spawns subagents** — one per competitor, researching in parallel

**💾 Saves findings** to a virtual filesystem so nothing is lost

**📊 Synthesizes** everything into a structured report

A regular agent would lose context and produce shallow output.
    """)

    st.markdown("---")
    st.caption("Model: OpenAI gpt-4o-mini  •  Search: Tavily")
    st.caption("Built with LangChain Deep Agents")

# ─────────────────────────────────────────────────────────────────────────────
# Main area
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("# Competitive Intelligence Agent")
st.markdown("*Type a research question. The agent plans, searches, and writes a full report.*")
st.markdown("---")

# Example queries
st.markdown("#### Quick start — click an example")

EXAMPLES = {
    "🗂 Project tools vs Jira":
        "Analyze Notion, Linear, and Asana as competitors to Atlassian Jira. "
        "Cover product features, pricing, customer sentiment, and recent strategic moves.",
    "🤖 AI coding tools":
        "Research GitHub Copilot, Cursor, and Windsurf as competitors in the AI coding assistant space. "
        "Compare features, pricing, user reviews, and recent news.",
    "🗄 Managed databases":
        "Compare Supabase, PlanetScale, and Neon as competitors in the managed database space. "
        "Focus on developer experience, pricing, and market positioning.",
}

col1, col2, col3 = st.columns(3)
for col, (label, query_text) in zip([col1, col2, col3], EXAMPLES.items()):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state["prefill"] = query_text

# Query input
query = st.text_area(
    "Your research query",
    value=st.session_state.get("prefill", ""),
    height=110,
    placeholder="e.g. Analyze Notion, Linear, and Asana as competitors to Jira — cover features, pricing, reviews, and recent news.",
)

run_btn = st.button(
    "🚀 Run Deep Agent",
    disabled=not keys_ok,
    use_container_width=False,
)

if not keys_ok:
    st.caption("← Add your API keys in the sidebar to enable the agent")

# ─────────────────────────────────────────────────────────────────────────────
# Agent execution
# ─────────────────────────────────────────────────────────────────────────────
if run_btn:
    if not query.strip():
        st.warning("Please enter a research query first.")
    else:
        st.markdown("---")
        st.markdown("### 🤖 Agent Running")

        st.markdown("""
<div class="log-box">
▶ Initializing deep agent with OpenAI gpt-4o-mini...<br>
📋 Agent will plan research tasks with write_todos...<br>
🔀 Subagents will be spawned per competitor...<br>
🔍 Searching: product features, pricing, reviews, news...<br>
💾 Saving findings to virtual filesystem...<br>
📊 Synthesizing final intelligence report...<br>
<br>
⏳ <strong style="color:#f7b731">This takes 1–3 minutes. Deep agents do thorough research.</strong>
</div>
""", unsafe_allow_html=True)

        progress = st.progress(0, text="Starting...")
        status_msg = st.empty()   # used for rate-limit countdown messages

        result_holder = {"output": None, "error": None, "rate_limit": None}

        def run_in_thread():
            from agent.deep_agent import run_agent, RateLimitError
            attempt = 0
            max_retries = 3
            while attempt < max_retries:
                try:
                    result_holder["output"] = run_agent(query)
                    result_holder["rate_limit"] = None
                    return
                except RateLimitError as e:
                    attempt = e.attempt
                    result_holder["rate_limit"] = {
                        "wait": e.wait_seconds,
                        "attempt": e.attempt,
                        "max_retries": e.max_retries,
                    }
                    time.sleep(e.wait_seconds)
                    result_holder["rate_limit"] = None  # clear after waiting
                except Exception as e:
                    result_holder["error"] = str(e)
                    return

        thread = threading.Thread(target=run_in_thread, daemon=True)
        thread.start()

        tick = 0
        while thread.is_alive():
            tick += 1

            # If we're in a rate-limit wait, show countdown
            rl = result_holder.get("rate_limit")
            if rl:
                remaining = max(0, rl["wait"] - (tick % rl["wait"]))
                status_msg.markdown(f"""
<div class="rate-limit-box">
⚠️ OpenAI rate limit hit (attempt {rl['attempt']}/{rl['max_retries']})<br>
⏳ Waiting {remaining}s before retrying automatically...<br>
💡 Tip: upgrade your OpenAI plan for higher limits →
<a href="https://platform.openai.com/account/rate-limits" target="_blank" style="color:#f7b731">
platform.openai.com/account/rate-limits</a>
</div>
""", unsafe_allow_html=True)
            else:
                status_msg.empty()

            pct = min(int((tick / 150) * 90), 90)
            progress.progress(pct, text=f"Researching... ({tick}s elapsed)")
            time.sleep(1)

        thread.join()
        progress.progress(100, text="Complete!")
        status_msg.empty()

        if result_holder["error"]:
            st.error(f"❌ Agent error:\n\n{result_holder['error']}")
            st.info(
                "Common fixes:\n"
                "- If you see 429: your OpenAI account has hit its rate limit. "
                "Wait a minute and try again, or upgrade your plan.\n"
                "- Check your API keys are correct\n"
                "- Make sure `pip install -r requirements.txt` ran successfully\n"
                "- Check your OpenAI account has credits at https://platform.openai.com/usage"
            )
        else:
            report = result_holder["output"]

            st.success("✅ Research complete!")
            st.download_button(
                label="⬇️ Download Report as Markdown",
                data=report,
                file_name="competitive_intel_report.md",
                mime="text/markdown",
            )

            st.markdown("---")
            st.markdown("### 📋 Intelligence Report")
            st.markdown('<div class="report-box">', unsafe_allow_html=True)
            st.markdown(report)
            st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("#### Why deep agents matter for competitive research")

c1, c2, c3, c4 = st.columns(4)
cards = [
    ("📋 Planning", "Breaks 'analyze 3 competitors' into 12+ specific research tasks before touching a single search."),
    ("🔀 Subagents", "Spawns a dedicated child agent per competitor — they research in parallel, not one after another."),
    ("💾 Filesystem", "Writes large search results to a virtual filesystem — never loses context across dozens of tool calls."),
    ("📊 Synthesis", "Reads all saved findings and compiles a cross-referenced, structured report with a competitive matrix."),
]
for col, (title, desc) in zip([c1, c2, c3, c4], cards):
    with col:
        st.markdown(
            f'<div class="how-card"><strong>{title}</strong><br>'
            f'<small style="color:#6b7280">{desc}</small></div>',
            unsafe_allow_html=True,
        )