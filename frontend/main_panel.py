import streamlit as st
from core.chains import run_chain

def render_main_panel():
    st.header("Research Gap Finder")
    st.caption("Analyze your uploaded research papers using Generative AI.")

    st.divider()

    # Guard: No papers ingested yet 
    if "processed_files" not in st.session_state or not st.session_state.processed_files:
        st.info(":point_left: Upload and process your research papers from the sidebar to get started.")
        return

    mode = st.session_state.get("selected_mode", "gap_finder")

    # Gap Finder & Contradiction Detector 
    if mode in ("gap_finder", "contradiction_detector"):
        mode_titles = {
            "gap_finder": "Research Gap Analysis",
            "contradiction_detector": "Contradiction Detection",
        }
        st.subheader(mode_titles[mode])

        default_questions = {
            "gap_finder": "What are the research gaps in the uploaded papers?",
            "contradiction_detector": "What are the contradictions between the uploaded papers?",
        }

        if st.button("Run Analysis", type="primary"):
            with st.spinner("Analyzing papers..."):
                response = run_chain(
                    mode=mode,
                    question=default_questions[mode],
                )
            st.markdown(response)

    # General Q&A
    elif mode == "qa":
        st.subheader("General Q&A")

        # Initialize chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        user_question = st.chat_input("Ask anything about your uploaded papers...")

        if user_question:
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_question)
            st.session_state.chat_history.append({
                "role": "user",
                "content": user_question,
            })

            # Generate and display response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = run_chain(
                        mode="qa",
                        question=user_question,
                    )
                st.markdown(response)

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": response,
            })