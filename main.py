import streamlit as st
from langgraph.types import Command
from pathlib import Path
from graph import app  
import uuid

# Session state variables
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]
if "state" not in st.session_state:
    st.session_state.state = None
if "interrupted" not in st.session_state:
    st.session_state.interrupted = False
if "resume_prompt" not in st.session_state:
    st.session_state.resume_prompt = ""

st.title("🎬 YouTube Shorts Generator")
st.markdown("---")
st.markdown(f"**Session ID**: `{st.session_state.thread_id}`")

# Run the graph on first button click
if st.button("🚀 Start Video Creation"):
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    result = app.invoke({}, config=config)
    st.session_state.state = result
    st.session_state.config = config
    st.session_state.interrupted = "__interrupt__" in result
    st.rerun()

# If there's an interrupt (human approval required)
if st.session_state.interrupted:
    interrupt = st.session_state.state["__interrupt__"][0]
    st.warning("🛑 Human Approval Required")

    # Display interrupt message
    st.markdown(f"**🔔 Prompt:** {interrupt.value}")

    # Show video preview if available
    video_path = st.session_state.state.get("video_path")
    if video_path and Path(video_path).exists():
        st.video(str(video_path))

    # Resume input form
    with st.form("resume_form"):
        user_input = st.radio("Your Response", ["yes", "no"], index=0)
        submitted = st.form_submit_button("Submit Response")

        if submitted:
            resumed = app.invoke(
                Command(resume=user_input),
                config=st.session_state.config
            )
            st.session_state.state = resumed
            st.session_state.interrupted = "__interrupt__" in resumed
            st.rerun()

# If graph execution is complete and no more interrupts
if st.session_state.state and not st.session_state.interrupted:
    st.success("✅ Process completed!")

    final = st.session_state.state

    if final.get("upload_success") is True:
        st.balloons()
        st.success("🎉 Video uploaded successfully!")
        st.markdown(f"🔗 **YouTube URL**: {final.get('youtube_url')}")
    elif final.get("upload_success") is False:
        st.error("❌ Upload failed")
        st.markdown(f"**Error**: {final.get('upload_error', 'Unknown error')}")
    else:
        st.warning("⚠️ Upload status unclear")

    # Final state dump
    with st.expander("📦 Final State"):
        st.json({k: v for k, v in final.items() if k != "__interrupt__"})
