# Handle SQLite for ChromaDB
try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except (ImportError, KeyError):
    pass


import streamlit as st
from utils.output_handler import capture_output
from main import main_crew
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()


# Configure the page
st.set_page_config(
    page_title="CrewAI Research Assistant",
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar menu
with st.sidebar:
    col1, col2, col3 = st.columns([0.1, 3.8, 0.1])
    with col2:
        st.image("https://cdn.prod.website-files.com/6481bf7bc1b01843dd1ced2b/6486e1c21b809d25782b7554_LATENTBRIDGE%20LOGO3%20TRANSPARENT%20(1)%203.png", width=220)
        st.header("Pre-Sales Agent Crew")
        page = st.text("Our Pre-Sales Agent Crew specializes in comprehensive research services tailored to your needs. " \
        "Currently, we offer detailed company research to provide you with the insights and data necessary to make informed " \
        "decisions and drive your business forward. Stay tuned for user research and product research, coming soon!")

# Main layout
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.title("🔍 Company Research Agent", anchor=False)


input_col1, input_col2, input_col3 = st.columns([1, 2, 1])
with input_col2:
    user_input = st.text_input("Please provide the name of the company you'd like me to research")

col1, col2, col3 = st.columns([1, 0.5, 1])
with col2:
    start_research = st.button("🚀 Start Research", use_container_width=False, type="primary")

result_text = ""
if start_research and user_input.strip():
    with st.status("🤖 Researching...", expanded=True) as status:
        try:
            # Create persistent container for process output with fixed height.
            process_container = st.container(height=300, border=True)
            output_container = process_container.container()
            
            # Single output capture context.
            with capture_output(output_container):
                result = main_crew.startCrew(user_input)
                status.update(label="✅ Research completed!", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Error occurred", state="error")
            st.error(f"An error occurred: {str(e)}")
            st.stop()
    # Convert CrewOutput to string for display and download
    result_text = str(result)
    # Display the final result
    st.markdown(result_text)

    # Create download buttons
    st.divider()
    download_col1, download_col2, download_col3 = st.columns([1, 2, 1])
    with download_col2:
        st.markdown("### 📥 Download Research Report")
        
    # Download as Markdown
    st.download_button(
        label="Download Report",
        data=result_text,
        file_name="research_report.md",
        mime="text/markdown",
        help="Download the research report in Markdown format"
        )


elif start_research:
        st.warning("Please enter a valid company name.")

# Add footer
st.divider()