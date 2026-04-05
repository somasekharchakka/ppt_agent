"""
app.py — Streamlit dashboard for the Auto-PPT Agent.
Features: template selector, slide count slider, live progress, download button.
"""
import streamlit as st
import asyncio
import os
import sys

# Allow importing from servers/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "servers"))

from agent_ppt import run_ppt_agent
from templates import TEMPLATES, get_template_names

# ─── Page configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Auto PPT Agent",
    page_icon="✨",
    layout="centered",
)

# ─── Custom CSS for a polished look ──────────────────────────────────────────
st.markdown("""
<style>
    /* Main title gradient */
    .main-title {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #a0a0b0;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    /* Template preview cards */
    .theme-card {
        border: 1px solid #333;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 8px;
    }
    .theme-name { font-weight: 700; font-size: 1rem; }
    .theme-meta { font-size: 0.82rem; color: #999; }
    /* Download button override */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1, #a855f7);
        color: white !important;
        font-weight: 600;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 10px;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #4f46e5, #9333ea);
    }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar – Settings ──────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    template_keys = get_template_names()
    template_labels = {k: TEMPLATES[k]["display_name"] for k in template_keys}
    selected_template = st.selectbox(
        "Visual Template",
        options=template_keys,
        format_func=lambda k: template_labels[k],
        index=template_keys.index("corporate_professional"),
        help="Choose a color theme for the generated slides.",
    )

    slide_count = st.slider(
        "Number of Slides",
        min_value=3,
        max_value=10,
        value=5,
        help="How many content slides the agent should create.",
    )

    st.divider()

    # Theme preview
    theme = TEMPLATES[selected_template]
    st.markdown("**Theme Preview**")
    bg = theme["bg_color"]
    accent = theme["accent_color"]
    title_c = theme["title_color"]
    title_bg = theme["title_bg"]
    st.markdown(
        f"""
        <div style="border-radius:10px; overflow:hidden; border:1px solid #444;">
            <div style="background:rgb{title_bg}; padding:10px 14px;">
                <span style="color:rgb{title_c}; font-weight:700; font-size:0.95rem;">
                    {theme['display_name']}
                </span>
            </div>
            <div style="background:rgb{bg}; padding:12px 14px;">
                <span style="color:rgb{theme['content_color']}; font-size:0.85rem;">
                    ▸ Sample bullet point<br>
                    ▸ Another bullet point
                </span>
            </div>
            <div style="background:rgb{accent}; height:6px;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("Built with LangChain, MCP, and Streamlit")

# ─── Main content area ───────────────────────────────────────────────────────
st.markdown('<div class="main-title">✨ Auto PPT Agent</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Generate professional PowerPoint presentations using AI.</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([3, 1])
with col1:
    prompt = st.text_area(
        "📄 Presentation Topic",
        value=f"Create a {slide_count} slide presentation on Large Language Models",
        height=100,
    )
with col2:
    st.markdown(f"**Template:** `{selected_template}`")
    st.markdown(f"**Slides:** `{slide_count}`")

generate = st.button("🚀 Generate Presentation", use_container_width=True)

# ─── Generation logic ────────────────────────────────────────────────────────
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.pptx")

if generate:
    if not prompt.strip():
        st.warning("Please enter a topic first.")
    else:
        # Delete old file so we can detect success
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

        with st.status("🤖 Agent is working …", expanded=True) as status:
            try:
                st.write(f"📋 **Template:** {template_labels[selected_template]}")
                st.write(f"📊 **Slides:** {slide_count}")
                st.write("🔍 Researching topic …")

                result = asyncio.run(
                    run_ppt_agent(
                        user_request=prompt,
                        template=selected_template,
                        slide_count=slide_count,
                    )
                )

                if os.path.exists(OUTPUT_FILE):
                    fsize = os.path.getsize(OUTPUT_FILE)
                    status.update(
                        label=f"✅ Presentation saved ({fsize:,} bytes)",
                        state="complete",
                        expanded=False,
                    )
                    st.success("The agent has finished the task!")
                    if result and result.get("output"):
                        st.markdown(f"**Agent:** {result['output']}")

                    st.subheader("🎉 Your PPT is Ready!")
                    with open(OUTPUT_FILE, "rb") as fp:
                        st.download_button(
                            label="⬇️ Download Presentation",
                            data=fp,
                            file_name="output.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            use_container_width=True,
                        )
                else:
                    status.update(label="⚠️ File not found", state="error")
                    st.warning(
                        "Agent finished, but the .pptx file was not found. "
                        "Check terminal logs for [DEBUG] messages.",
                        icon="⚠️",
                    )

            except Exception as exc:
                status.update(label="❌ Error", state="error")
                st.error(f"Error: {exc}")
