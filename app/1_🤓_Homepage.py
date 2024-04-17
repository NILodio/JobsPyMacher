import os

import streamlit as st
from streamlit_extras import add_vertical_space as add_vertical_space
from streamlit_extras.badges import badge
from utils import update_st_state

# Set page configuration
st.set_page_config(
    page_title="JobsPy Matcher",
    initial_sidebar_state="auto",
    layout="wide",
)

# Initialize session state variables if not present
session_state_keys = [
    "resume_uploaded",
    "resume_path",
    "job_description_uploaded",
    "job_description_path",
]
for key in session_state_keys:
    if key not in st.session_state.keys():
        update_st_state(key, "Pending")

# Main content
st.title(":blue[JobsPy Matcher]")

# Sidebar
with st.sidebar:
    st.subheader(
        "JobsPy Matcher is a Resume Matcher that uses NLP to match your resume with job descriptions."
    )
    st.markdown(
        "Give JobsPy Matcher a ⭐ on [GitHub](https://github.com/NILodio/JobsPyMatcher)"
    )
    badge(type="github", name="NILodio/JobsPyMatcher")

# Divider and vertical space
st.divider()
add_vertical_space(1)

with st.container():
    resume_col, job_description_col = st.columns(2)
    with resume_col:
        uploaded_resume = st.file_uploader("Choose a Resume", type="pdf")
        if uploaded_resume is not None:
            if st.session_state["resume_uploaded"] == "Pending":
                save_path_resume = os.path.join(
                    "data", "app", "resumes", uploaded_resume.name
                )

                with open(save_path_resume, mode="wb") as w:
                    w.write(uploaded_resume.getvalue())

                if os.path.exists(save_path_resume):
                    st.toast(
                        f"File {uploaded_resume.name} is successfully saved!", icon="✔️"
                    )
                    update_st_state("resume_uploaded", "Uploaded")
                    update_st_state("resume_path", save_path_resume)
        else:
            update_st_state("resume_uploaded", "Pending")
            update_st_state("resume_path", "")

    with job_description_col:
        uploaded_job_description = st.file_uploader(
            "Choose a Job Description", type="pdf"
        )
        if uploaded_job_description is not None:
            if st.session_state["job_description_uploaded"] == "Pending":
                save_path_job_description = os.path.join(
                    "data", "app", "jobdescription", uploaded_job_description.name
                )
                with open(save_path_job_description, mode="wb") as w:
                    w.write(uploaded_job_description.getvalue())

                if os.path.exists(save_path_job_description):
                    st.toast(
                        f"File {uploaded_job_description.name} is successfully saved!",
                        icon="✔️",
                    )
                    update_st_state("job_description_uploaded", "Uploaded")
                    update_st_state("job_description_path", save_path_job_description)
        else:
            update_st_state("job_description_uploaded", "Pending")
            update_st_state("job_description_path", "")
