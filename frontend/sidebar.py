import streamlit as st
from core.ingestion import process_pdf
from utils.helpers import save_uploaded_file

MODES = {
    "Gap Finder": "gap_finder",
    "Contradiction Detector": "contradiction_detector",
    "General Q&A": "qa",
}

def render_sidebar():
    with st.sidebar:
        st.title(":telescope: Research Gap Finder")
        st.caption("Upload research papers and analyze them using AI.")

        st.divider()

        # File Uploader 
        st.subheader("Upload Papers")
        uploaded_files = st.file_uploader(
            label="Upload PDF research papers",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        # Process Button
        if uploaded_files:
            if st.button("Process Papers", type="primary", use_container_width=True):
                if "processed_files" not in st.session_state:
                    st.session_state.processed_files = []

                progress_bar = st.progress(0)
                status_text = st.empty()
                total = len(uploaded_files)

                for i, uploaded_file in enumerate(uploaded_files):
                    if uploaded_file.name not in st.session_state.processed_files:
                        status_text.info(f"Processing {uploaded_file.name} ({i+1}/{total})...")
                        file_path = save_uploaded_file(uploaded_file)
                        result = process_pdf(file_path)

                        if isinstance(result, str):
                            status_text.warning(result)
                        else:
                            st.session_state.processed_files.append(uploaded_file.name)
                            status_text.success(f"{uploaded_file.name} ingested!")
                    else:
                        status_text.warning(f"{uploaded_file.name} already ingested, skipping...")

                    progress_bar.progress((i + 1) / total)

                status_text.success("All papers processed!")
                progress_bar.empty()

        st.divider()

        # Uploaded Papers List 
        if "processed_files" in st.session_state and st.session_state.processed_files:
            st.subheader("Ingested Papers")
            for paper in st.session_state.processed_files:
                st.markdown(f"- :open_book: `{paper}`")

            st.divider()

        # Mode Selector 
        st.subheader("Analysis Mode")
        selected_label = st.selectbox(
            label="Select a mode",
            options=list(MODES.keys()),
            label_visibility="collapsed",
        )

        st.session_state.selected_mode = MODES[selected_label]

        # Mode Descriptions
        mode_descriptions = {
            "gap_finder": "Identifies underexplored topics, missing methodologies, and future research directions.",
            "contradiction_detector": "Finds conflicting findings and disagreements between the uploaded papers.",
            "qa": "Ask any question and get a cited answer grounded in your uploaded papers.",
        }
        st.caption(mode_descriptions[st.session_state.selected_mode])