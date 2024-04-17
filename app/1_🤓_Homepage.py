import os
import pandas as pd
import streamlit as st
from streamlit_extras import add_vertical_space as avs
import plotly.express as px
import plotly.graph_objects as go
from annotated_text import annotated_text
from streamlit_extras.badges import badge
from utils import update_st_state, create_annotated_text, create_star_graph

from jobsparser import ParseJobDesc, ParseResume, TextUtils

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
avs.add_vertical_space(1)

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

with st.spinner("Please wait..."):
    if (
        uploaded_resume is not None
        and st.session_state["job_description_uploaded"] == "Uploaded"
        and uploaded_job_description is not None
        and st.session_state["job_description_uploaded"] == "Uploaded"
    ):
        resume_processor = ParseResume(
            TextUtils().read_single_pdf(st.session_state["resume_path"])
        )
        job_description_processor = ParseJobDesc(
            TextUtils().read_single_pdf(st.session_state["job_description_path"])
        )

        selected_file = resume_processor.get_JSON()
        selected_jd = job_description_processor.get_JSON()

        with st.container():
            resumeCol, jobDescriptionCol = st.columns(2)
            with resumeCol:
                with st.expander("Parsed Resume Data"):
                    st.caption("This text is parsed from your resume.")
                    avs.add_vertical_space(3)
                    st.write(selected_file["clean_data"])

            with jobDescriptionCol:
                with st.expander("Parsed Job Description"):
                    st.caption("parsing from PDF but it'll be from txt or copy paste.")
                    avs.add_vertical_space(3)
                    st.write(selected_jd["clean_data"])

        with st.container():
            resumeCol, jobDescriptionCol = st.columns(2)
            with resumeCol:
                with st.expander("Extracted Keywords"):
                    st.write(
                        "Now let's take a look at the extracted keywords from the resume."
                    )
                    annotated_text(
                        create_annotated_text(
                            selected_file["clean_data"],
                            selected_file["extracted_keywords"],
                            "KW",
                            "#CCFFFF",
                        )
                    )
            with jobDescriptionCol:
                with st.expander("Extracted Keywords"):
                    st.write(
                        "Now let's take a look at the extracted keywords from the job description."
                    )
                    annotated_text(
                        create_annotated_text(
                            selected_jd["clean_data"],
                            selected_jd["extracted_keywords"],
                            "KW",
                            "#0B666A",
                        )
                    )

        with st.container():
            resumeCol, jobDescriptionCol = st.columns(2)
            with resumeCol:
                with st.expander("Extracted Entities"):
                    st.write(
                        "Now let's take a look at the extracted entities from the resume."
                    )
                    create_star_graph(selected_file["keyterms"], "Entities from Resume")
            with jobDescriptionCol:
                with st.expander("Extracted Entities"):
                    st.write(
                        "Now let's take a look at the extracted entities from the job description."
                    )
                    create_star_graph(
                        selected_jd["keyterms"], "Entities from Job Description"
                    )

        with st.container():
            resumeCol, jobDescriptionCol = st.columns(2)
            with resumeCol:
                with st.expander("Keywords & Values"):
                    df1 = pd.DataFrame(
                        selected_file["keyterms"], columns=["keyword", "value"]
                    )
                    keyword_dict = {}
                    for keyword, value in selected_file["keyterms"]:
                        keyword_dict[keyword] = value * 100

                    fig = go.Figure(
                        data=[
                            go.Table(
                                header=dict(
                                    values=["Keyword", "Value"],
                                    font=dict(size=12, color="white"),
                                    fill_color="#1d2078",
                                ),
                                cells=dict(
                                    values=[
                                        list(keyword_dict.keys()),
                                        list(keyword_dict.values()),
                                    ],
                                    line_color="darkslategray",
                                    fill_color="#6DA9E4",
                                ),
                            )
                        ]
                    )
                    st.plotly_chart(fig, use_container_width=True)
            with jobDescriptionCol:
                with st.expander("Keywords & Values"):
                    df2 = pd.DataFrame(
                        selected_jd["keyterms"], columns=["keyword", "value"]
                    )

                    # Create the dictionary
                    keyword_dict = {}
                    for keyword, value in selected_jd["keyterms"]:
                        keyword_dict[keyword] = value * 100

                    fig = go.Figure(
                        data=[
                            go.Table(
                                header=dict(
                                    values=["Keyword", "Value"],
                                    font=dict(size=12, color="white"),
                                    fill_color="#1d2078",
                                ),
                                cells=dict(
                                    values=[
                                        list(keyword_dict.keys()),
                                        list(keyword_dict.values()),
                                    ],
                                    line_color="darkslategray",
                                    fill_color="#6DA9E4",
                                ),
                            )
                        ]
                    )
                    st.plotly_chart(fig, use_container_width=True)

        with st.container():
            resumeCol, jobDescriptionCol = st.columns(2)
            with resumeCol:
                with st.expander("Key Topics"):
                    fig = px.treemap(
                        df1,
                        path=["keyword"],
                        values="value",
                        color_continuous_scale="Rainbow",
                        title="Key Terms/Topics Extracted from your Resume",
                    )
                    st.plotly_chart(fig, use_container_width=True)

            with jobDescriptionCol:
                with st.expander("Key Topics"):
                    fig = px.treemap(
                        df2,
                        path=["keyword"],
                        values="value",
                        color_continuous_scale="Rainbow",
                        title="Key Terms/Topics Extracted from Job Description",
                    )
                    st.plotly_chart(fig, use_container_width=True)

st.divider()
st.markdown("[:arrow_up: Back to Top](#resume-matcher)")
