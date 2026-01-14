"""
Resume Keyword Matcher - Main Application
A modern web application to analyze resumes against job descriptions using AI
"""

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv

# Import utility modules
from utils.pdf_extractor import extract_text_from_pdf, validate_pdf, get_file_info
from utils.gemini_analyzer import (
    analyze_resume_with_gemini,
    analyze_resume_with_groq,
    get_match_rating,
)
from utils.report_generator import create_analysis_report
from utils.email_sender import (
    send_analysis_email,
    validate_email,
    get_smtp_config_instructions,
)
from utils.resume_analyzer import (
    analyze_resume_length,
    validate_contact_information,
    count_bullet_points,
    analyze_action_verbs,
    generate_wordcloud,
    check_quantification,
    calculate_readability_score,
    create_keyword_density_map,
    export_analysis_to_dict,
    detect_resume_sections,
    check_date_formats,
    find_duplicate_content,
    validate_ats_format,
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Resume Keyword Matcher",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Custom CSS
def load_custom_css():
    """Load custom CSS for modern styling"""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
    }
    
    [data-testid="stHeader"] {
        background: #ffffff !important;
    }
    
    /* Force all text to be visible */
    .stApp * {
        color: #1e293b !important;
    }
    
    .stApp label {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* Input fields */
    input, textarea, select {
        color: #1e293b !important;
        background: #ffffff !important;
    }
    
    /* Radio buttons and checkboxes */
    .stRadio label, .stCheckbox label {
        color: #1e293b !important;
    }
    
    /* Radio button custom styling */
    .stRadio > div {
        background: transparent !important;
    }
    
    .stRadio div[role="radiogroup"] > label {
        background: #ffffff !important;
        border: 2px solid #e5e7eb !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0 !important;
        color: #1e293b !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }
    
    .stRadio div[role="radiogroup"] > label:hover {
        background: #f0f9ff !important;
        border-color: #0ea5e9 !important;
    }
    
    /* Radio button circle */
    .stRadio input[type="radio"] {
        accent-color: #0ea5e9 !important;
        width: 20px !important;
        height: 20px !important;
        cursor: pointer !important;
    }
    
    /* Selected radio button */
    .stRadio div[data-baseweb="radio"] > div:first-child {
        border-color: #0ea5e9 !important;
        background-color: #0ea5e9 !important;
    }
    
    .stRadio div[data-baseweb="radio"] > div:first-child > div {
        background-color: #ffffff !important;
    }
    
    /* File uploader text */
    .stFileUploader label, .stFileUploader span {
        color: #1e293b !important;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 2rem 1rem;
        background: #0ea5e9;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 20px rgba(14, 165, 233, 0.15);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        font-weight: 400;
        opacity: 0.95;
    }
    
    /* Card styling */
    .custom-card {
        background: #f9fafb;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Score display */
    .score-container {
        text-align: center;
        padding: 2rem;
        background: #f0f9ff;
        border-radius: 12px;
        border: 2px solid #0ea5e9;
        color: #0c4a6e;
        margin: 2rem 0;
    }
    
    .score-value {
        font-size: 4rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    .score-label {
        font-size: 1.5rem;
        opacity: 0.9;
    }
    
    /* Keyword pills */
    .keyword-pill {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        background: #e0f2fe;
        color: #0369a1;
        border: 1px solid #0ea5e9;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .missing-keyword-pill {
        background: #fee2e2;
        color: #991b1b;
        border: 1px solid #ef4444;
    }
    
    /* Success/Warning/Error boxes */
    .success-box {
        background: #dcfce7;
        color: #166534;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fef3c7;
        color: #92400e;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .error-box {
        background: #fee2e2;
        color: #991b1b;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    #f9fafb;
        border-radius: 12px;
        margin: 1rem;
        border: 1px solid #e5e7eb;
    }
    
    .step-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .step-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #0c4a6e;
        margin-bottom: 0.5rem;
    }
    
    .step-description {
        font-size: 0.95rem;
        color: #64748b;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: #0ea5e9 !important;
        color: white !important;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #0284c7 !important;
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.2);
        color: white !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: #f9fafb !important;
        border-radius: 8px;
        padding: 1rem;
        border: 2px dashed #cbd5e1;
        color: #1e293b !important;
    }
    
    .stFileUploader > div > div {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Drag and drop area */
    .stFileUploader section {
        background: #f8fafc !important;
        border-radius: 8px !important;
        border: 2px dashed #cbd5e1 !important;
    }
    
    .stFileUploader section > div {
        color: #1e293b !important;
    }
    
    .stFileUploader section span {
        color: #1e293b !important;
    }
    
    .stFileUploader small {
        color: #64748b !important;
    }
    
    /* File uploader text inside drag area */
    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: #f8fafc !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzone"] span {
        color: #1e293b !important;
    }
    
    .stFileUploader [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #1e293b !important;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        padding: 1rem;
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #0ea5e9;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1);
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e2e8f0;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #1e293b !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #1e293b !important;
    }
    
    /* Sidebar inputs */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] select,
    section[data-testid="stSidebar"] textarea {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* Main content text colors */
    .stApp p, .stApp span, .stApp label {
        color: #1e293b !important;
    }
    
    /* Text input fields */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    .stTextInput label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Password input */
    input[type="password"] {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Password visibility toggle */
    .stTextInput button {
        background: #ffffff !important;
        border: none !important;
        border-left: 1px solid #e5e7eb !important;
        border-radius: 0 8px 8px 0 !important;
        color: #1e293b !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 100% !important;
        width: 60px !important;
        min-width: 60px !important;
        max-width: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }
    
    .stTextInput button:hover {
        background: #0ea5e9 !important;
        border-left-color: #0ea5e9 !important;
        color: #ffffff !important;
        width: 60px !important;
    }
    
    .stTextInput button svg {
        color: #1e293b !important;
        fill: #1e293b !important;
        width: 20px !important;
        height: 20px !important;
        margin: 0 auto !important;
    }
    
    .stTextInput button:hover svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    
    /* Input field adjustment */
    .stTextInput input {
        border-radius: 8px 0 0 8px !important;
    }
    
    /* Input wrapper - remove any dark backgrounds */
    .stTextInput > div > div {
        background: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stTextInput div[data-baseweb="input"] {
        background: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stTextInput div[data-baseweb="base-input"] {
        background: #ffffff !important;
        border-radius: 8px !important;
    }
    
    .stTextInput div[data-baseweb="base-input"] > div {
        background: #ffffff !important;
    }
    
    /* Remove container backgrounds */
    .stTextInput div[data-baseweb="base-input"] > div:last-child {
        background: #ffffff !important;
    }
    
    .stTextInput [data-baseweb="input"] button {
        background: #ffffff !important;
        border: none !important;
        border-left: 1px solid #e5e7eb !important;
        border-radius: 0 8px 8px 0 !important;
        margin: 0 !important;
        width: 60px !important;
        min-width: 60px !important;
        max-width: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }
    
    .stTextInput [data-baseweb="input"] button:hover {
        background: #0ea5e9 !important;
        border-left-color: #0ea5e9 !important;
        width: 60px !important;
    }
    
    /* Tooltip for password toggle */
    div[role="tooltip"] {
        background: #1e293b !important;
        color: #ffffff !important;
        padding: 0.5rem 1rem !important;
        border-radius: 6px !important;
        font-size: 0.875rem !important;
    }
    
    /* Streamlit tooltip */
    .stTooltipIcon {
        color: #64748b !important;
    }
    
    [data-baseweb="tooltip"] {
        background: #1e293b !important;
        color: #ffffff !important;
    }
    
    [data-baseweb="tooltip"] div {
        color: #ffffff !important;
    }
    
    /* Select box styling */
    .stSelectbox {
        color: #1e293b !important;
    }
    
    .stSelectbox label {
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox > div > div {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    .stSelectbox select {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Dropdown menu options */
    div[role="listbox"] {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    div[role="option"] {
        background: #ffffff !important;
        color: #1e293b !important;
        padding: 0.5rem 1rem !important;
    }
    
    div[role="option"]:hover {
        background: #f0f9ff !important;
        color: #0369a1 !important;
    }
    
    /* Selectbox dropdown */
    ul[role="listbox"] {
        background: #ffffff !important;
    }
    
    li[role="option"] {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    li[role="option"]:hover {
        background: #f0f9ff !important;
        color: #0369a1 !important;
    }
    
    /* Dropdown container */
    div[data-baseweb="popover"] {
        background: #ffffff !important;
    }
    
    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    /* Radio buttons */
    .stRadio > div {
        background: transparent !important;
    }
    
    .stRadio label {
        color: #1e293b !important;
    }
    
    /* File uploader button */
    .stFileUploader button {
        background: #0ea5e9 !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1.5rem !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    
    .stFileUploader button:hover {
        background: #0284c7 !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: white !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #f1f5f9 !important;
        border-radius: 8px;
        color: #475569 !important;
        border: 1px solid #cbd5e1;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0ea5e9 !important;
        color: white !important;
        border-color: #0ea5e9;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #e0f2fe !important;
        color: #0369a1 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #f8fafc !important;
        color: #1e293b !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        font-weight: 600 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f0f9ff !important;
        color: #0369a1 !important;
    }
    
    details summary {
        color: #1e293b !important;
        background: #f8fafc !important;
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
    }
    
    details summary:hover {
        background: #f0f9ff !important;
        color: #0369a1 !important;
    }
    
    details[open] summary {
        color: #0369a1 !important;
        background: #f0f9ff !important;
    }
    
    /* Expander content */
    .streamlit-expanderContent {
        background: #ffffff !important;
        color: #1e293b !important;
    }
    
    details div {
        color: #1e293b !important;
    }
    
    /* Sidebar expanders */
    section[data-testid="stSidebar"] details summary {
        color: #1e293b !important;
        background: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] details summary:hover {
        background: #f0f9ff !important;
        color: #0369a1 !important;
    }
    
    section[data-testid="stSidebar"] details[open] summary {
        background: #f0f9ff !important;
        color: #0369a1 !important;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Override any dark theme */
.animate-fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }
        
        .custom-card {
            background: rgba(30, 41, 59, 0.95);
            color: #f1f5f9;
        }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def create_hero_section():
    """Create the hero section"""
    st.markdown(
        """
        <div class="hero-section animate-fade-in">
            <div class="hero-title">📄 Resume Keyword Matcher</div>
            <div class="hero-subtitle">Optimize your resume for job applications with AI-powered analysis</div>
        </div>
    """,
        unsafe_allow_html=True,
    )


def create_how_it_works():
    """Create how it works section"""
    st.markdown("### 🎯 How It Works")

    cols = st.columns(4)

    with cols[0]:
        st.markdown(
            """
            <div class="step-container">
                <div class="step-icon">📤</div>
                <div class="step-title">1. Upload Resume</div>
                <div class="step-description">Upload your resume in PDF format</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with cols[1]:
        st.markdown(
            """
            <div class="step-container">
                <div class="step-icon">📝</div>
                <div class="step-title">2. Paste Job Description</div>
                <div class="step-description">Copy and paste the job posting</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with cols[2]:
        st.markdown(
            """
            <div class="step-container">
                <div class="step-icon">🤖</div>
                <div class="step-title">3. AI Analysis</div>
                <div class="step-description">Get instant AI-powered insights</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    with cols[3]:
        st.markdown(
            """
            <div class="step-container">
                <div class="step-icon">🎉</div>
                <div class="step-title">4. Improve & Apply</div>
                <div class="step-description">Optimize and download your report</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    add_vertical_space(2)


def create_gauge_chart(score: float) -> go.Figure:
    """Create a gauge chart for match score"""
    if score >= 71:
        color = "#10B981"
    elif score >= 41:
        color = "#F59E0B"
    else:
        color = "#EF4444"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Match Score", "font": {"size": 24, "color": "#0c4a6e"}},
            number={"font": {"size": 60, "color": color}},
            gauge={
                "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "darkgray"},
                "bar": {"color": color, "thickness": 0.75},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "gray",
                "steps": [
                    {"range": [0, 40], "color": "#fee2e2"},
                    {"range": [40, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#d1fae5"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 4},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"color": "#0c4a6e", "family": "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
    )

    return fig


def display_results(analysis_result: dict, resume_filename: str, key_suffix: str = ""):
    """Display analysis results in a beautiful format"""

    # Match Score Section
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    add_vertical_space(1)

    col1, col2 = st.columns([1, 2])

    with col1:
        # Gauge chart
        score = analysis_result.get("match_score", 0)
        fig = create_gauge_chart(score)
        st.plotly_chart(fig, width="stretch", key=f"gauge_chart{key_suffix}")

        rating, color = get_match_rating(score)
        st.markdown(
            f"""
            <div style="text-align: center; padding: 1rem; background: {color}; color: white; 
                        border-radius: 10px; font-size: 1.2rem; font-weight: 600;">
                {rating}
            </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("### 💡 Match Reasoning")
        st.info(analysis_result.get("match_reasoning", "No reasoning provided"))

        # Strengths
        if "strengths" in analysis_result and analysis_result["strengths"]:
            st.markdown("### ✨ Key Strengths")
            for strength in analysis_result["strengths"]:
                st.markdown(f"✅ {strength}")

    add_vertical_space(2)

    # Found Keywords Section
    st.markdown("### ✅ Keywords Found in Your Resume")
    found_keywords = analysis_result.get("found_keywords", {})

    tabs = st.tabs(["Technical Skills", "Soft Skills", "Experience", "Education"])

    with tabs[0]:
        if found_keywords.get("technical_skills"):
            keywords_html = "".join(
                [
                    f'<span class="keyword-pill">{keyword}</span>'
                    for keyword in found_keywords["technical_skills"]
                ]
            )
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.info("No technical skills identified")

    with tabs[1]:
        if found_keywords.get("soft_skills"):
            keywords_html = "".join(
                [
                    f'<span class="keyword-pill">{keyword}</span>'
                    for keyword in found_keywords["soft_skills"]
                ]
            )
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.info("No soft skills identified")

    with tabs[2]:
        if found_keywords.get("experience_keywords"):
            keywords_html = "".join(
                [
                    f'<span class="keyword-pill">{keyword}</span>'
                    for keyword in found_keywords["experience_keywords"]
                ]
            )
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.info("No experience keywords identified")

    with tabs[3]:
        if found_keywords.get("education_keywords"):
            keywords_html = "".join(
                [
                    f'<span class="keyword-pill">{keyword}</span>'
                    for keyword in found_keywords["education_keywords"]
                ]
            )
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.info("No education keywords identified")

    add_vertical_space(2)

    # Missing Keywords Section
    st.markdown("### ⚠️ Missing Keywords & Gaps")
    missing_keywords = analysis_result.get("missing_keywords", {})

    with st.expander("🔴 Critical Technical Skills", expanded=True):
        if missing_keywords.get("critical_technical_skills"):
            keywords_html = "".join(
                [
                    f'<span class="keyword-pill missing-keyword-pill">{keyword}</span>'
                    for keyword in missing_keywords["critical_technical_skills"]
                ]
            )
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.success("All critical technical skills covered!")

    with st.expander("🟡 Important Soft Skills"):
        if missing_keywords.get("important_soft_skills"):
            keywords_html = "".join(
                [
                    f'<span class="keyword-pill missing-keyword-pill">{keyword}</span>'
                    for keyword in missing_keywords["important_soft_skills"]
                ]
            )
            st.markdown(keywords_html, unsafe_allow_html=True)
        else:
            st.success("All important soft skills covered!")

    with st.expander("📋 Experience Gaps"):
        if missing_keywords.get("experience_gaps"):
            for gap in missing_keywords["experience_gaps"]:
                st.warning(f"• {gap}")
        else:
            st.success("No significant experience gaps!")

    with st.expander("🎓 Education Gaps"):
        if missing_keywords.get("education_gaps"):
            for gap in missing_keywords["education_gaps"]:
                st.warning(f"• {gap}")
        else:
            st.success("No education gaps!")

    add_vertical_space(2)

    # Suggestions Section
    st.markdown("### 🎯 Recommendations for Improvement")
    if "suggestions" in analysis_result and analysis_result["suggestions"]:
        for i, suggestion in enumerate(analysis_result["suggestions"], 1):
            st.markdown(
                f"""
                <div class="custom-card">
                    <strong>{i}.</strong> {suggestion}
                </div>
            """,
                unsafe_allow_html=True,
            )

    add_vertical_space(2)

    # ATS Tips Section
    st.markdown("### 🤖 ATS Optimization Tips")
    if (
        "ats_optimization_tips" in analysis_result
        and analysis_result["ats_optimization_tips"]
    ):
        for tip in analysis_result["ats_optimization_tips"]:
            st.info(f"💡 {tip}")

    add_vertical_space(2)

    # Download Report
    st.markdown("### 📥 Download Full Report")
    try:
        pdf_buffer = create_analysis_report(analysis_result, resume_filename)
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            width="stretch",
        )
    except Exception as e:
        st.error(f"Error generating PDF report: {str(e)}")


def display_additional_features(
    resume_text: str,
    analysis_result: dict = None,
    pdf_path: str = None,
    key_suffix: str = "",
):
    """Display additional resume analysis features"""
    st.markdown("---")
    st.markdown("## 🔍 Additional Analysis")
    add_vertical_space(1)

    # Create tabs for different features
    (
        tab1,
        tab2,
        tab3,
        tab4,
        tab5,
        tab6,
        tab7,
        tab8,
        tab9,
        tab10,
        tab11,
        tab12,
        tab13,
        tab14,
    ) = st.tabs(
        [
            "📏 Length",
            "📧 Contact",
            "📋 Bullets",
            "💪 Verbs",
            "☁️ Word Cloud",
            "📊 Metrics",
            "📖 Readability",
            "🔥 Keyword Density",
            "💾 Export",
            "📑 Sections",
            "📅 Dates",
            "🔄 Duplicates",
            "🤖 ATS Check",
            "📧 Email Results",
        ]
    )

    with tab1:
        st.markdown("### 📏 Resume Length Analysis")
        length_analysis = analyze_resume_length(resume_text)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Word Count", f"{length_analysis['word_count']:,}")
        with col2:
            st.metric("Characters", f"{length_analysis['character_count']:,}")
        with col3:
            st.metric("Estimated Pages", length_analysis["estimated_pages"])

        if length_analysis["status"] == "success":
            st.success(f"✅ {length_analysis['recommendation']}")
        else:
            st.warning(f"⚠️ {length_analysis['recommendation']}")

    with tab2:
        st.markdown("### 📧 Contact Information Validator")
        contact_analysis = validate_contact_information(resume_text)

        # Score display
        score = contact_analysis["score"]
        if score == 100:
            st.success(f"🎉 Perfect Score: {score}/100")
        elif score >= 75:
            st.success(f"✅ Good: {score}/100")
        else:
            st.warning(f"⚠️ Needs Improvement: {score}/100")

        # Contact details
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Present:**")
            if contact_analysis["email"]["present"]:
                st.success(f"✅ Email: {contact_analysis['email']['value']}")
            if contact_analysis["phone"]["present"]:
                st.success(f"✅ Phone: {contact_analysis['phone']['value']}")
            if contact_analysis["linkedin"]["present"]:
                st.success("✅ LinkedIn")
            if contact_analysis["github"]["present"]:
                st.success(f"✅ GitHub: {contact_analysis['github']['value']}")

        with col2:
            if contact_analysis["missing"]:
                st.markdown("**Missing:**")
                for missing in contact_analysis["missing"]:
                    st.error(f"❌ {missing}")

    with tab3:
        st.markdown("### 📋 Bullet Point Analysis")
        bullet_analysis = count_bullet_points(resume_text)

        st.metric("Total Bullet Points", bullet_analysis["total_count"])

        if bullet_analysis["status"] == "success":
            st.success(f"✅ {bullet_analysis['recommendation']}")
        else:
            st.warning(f"⚠️ {bullet_analysis['recommendation']}")

        if bullet_analysis["sample_bullets"]:
            with st.expander("📝 Sample Bullet Points"):
                for bullet in bullet_analysis["sample_bullets"]:
                    st.markdown(f"• {bullet}")

    with tab4:
        st.markdown("### 💪 Action Verb Analysis")
        verb_analysis = analyze_action_verbs(resume_text)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Strong Verbs", verb_analysis["strong_verbs_count"])
        with col2:
            st.metric("Weak Verbs", verb_analysis["weak_verbs_count"])
        with col3:
            st.metric("Score", f"{verb_analysis['score']}%")

        if verb_analysis["status"] == "success":
            st.success(f"✅ {verb_analysis['recommendation']}")
        else:
            st.warning(f"⚠️ {verb_analysis['recommendation']}")

        col1, col2 = st.columns(2)
        with col1:
            if verb_analysis["strong_verbs_used"]:
                st.markdown("**Strong Verbs Found:**")
                for verb in verb_analysis["strong_verbs_used"]:
                    st.markdown(
                        f'<span class="keyword-pill">{verb}</span>',
                        unsafe_allow_html=True,
                    )

        with col2:
            if verb_analysis["weak_verbs_found"]:
                st.markdown("**Weak Verbs to Replace:**")
                for verb in verb_analysis["weak_verbs_found"]:
                    st.markdown(
                        f'<span class="keyword-pill missing-keyword-pill">{verb}</span>',
                        unsafe_allow_html=True,
                    )

    with tab5:
        st.markdown("### ☁️ Resume Word Cloud")
        st.info("Visual representation of the most frequent words in your resume")

        try:
            wordcloud_img = generate_wordcloud(resume_text)
            st.image(wordcloud_img, width="stretch")
        except Exception as e:
            st.error(f"Error generating word cloud: {str(e)}")

    with tab6:
        st.markdown("### 📊 Quantification Analysis")
        quant_analysis = check_quantification(resume_text)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Metrics Found", quant_analysis["metrics_count"])
        with col2:
            st.metric("Quantified %", f"{quant_analysis['quantified_percentage']}%")

        if quant_analysis["status"] == "success":
            st.success(f"✅ {quant_analysis['recommendation']}")
        else:
            st.warning(f"⚠️ {quant_analysis['recommendation']}")

        if quant_analysis["sample_metrics"]:
            with st.expander("📈 Sample Metrics Found"):
                for metric in quant_analysis["sample_metrics"]:
                    st.markdown(f"• {metric}")

    with tab7:
        st.markdown("### 📖 Readability Score")
        readability = calculate_readability_score(resume_text)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Flesch Reading Ease", readability["flesch_score"])
        with col2:
            st.metric(
                "Avg Sentence Length", f"{readability['avg_sentence_length']} words"
            )
        with col3:
            st.metric("Avg Syllables/Word", readability["avg_syllables"])

        if readability["status"] == "success":
            st.success(f"✅ {readability['interpretation']}")
        else:
            st.warning(f"⚠️ {readability['interpretation']}")

        st.info(f"💡 {readability['recommendation']}")

    with tab8:
        st.markdown("### 🔥 Keyword Density Analysis")
        keyword_data = create_keyword_density_map(resume_text)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Words", f"{keyword_data['total_words']:,}")
        with col2:
            st.metric("Unique Words", f"{keyword_data['unique_words']:,}")

        st.markdown("**Top 20 Keywords:**")

        # Create a simple bar chart
        import plotly.graph_objects as go

        keywords = [kw[0] for kw in keyword_data["top_keywords"]]
        counts = [kw[1] for kw in keyword_data["top_keywords"]]

        fig = go.Figure(
            data=[
                go.Bar(
                    x=counts, y=keywords, orientation="h", marker=dict(color="#0ea5e9")
                )
            ]
        )

        fig.update_layout(
            title="Keyword Frequency",
            xaxis_title="Count",
            yaxis_title="Keyword",
            height=500,
            yaxis={"categoryorder": "total ascending"},
        )

        st.plotly_chart(fig, width="stretch")

    with tab9:
        st.markdown("### 💾 Export Analysis Data")
        st.info("Export your resume analysis to CSV format for tracking over time")

        if analysis_result:
            # Gather all additional analysis data
            additional_data = {
                "length": analyze_resume_length(resume_text),
                "contact": validate_contact_information(resume_text),
                "bullets": count_bullet_points(resume_text),
                "verbs": analyze_action_verbs(resume_text),
                "quantification": check_quantification(resume_text),
            }

            # Prepare export data
            export_data = export_analysis_to_dict(analysis_result, additional_data)

            # Convert to CSV format
            import pandas as pd
            import io

            df = pd.DataFrame([export_data])

            # Create CSV buffer
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_data = csv_buffer.getvalue()

            # Display preview
            st.markdown("**Preview:**")
            st.dataframe(df, width="stretch")

            # Download button
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                key=f"download_csv{key_suffix}",
            )

            # Excel export
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine="openpyxl")
            excel_data = excel_buffer.getvalue()

            st.download_button(
                label="📥 Download Excel",
                data=excel_data,
                file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=f"download_excel{key_suffix}",
            )
        else:
            st.warning(
                "Analysis data not available. Please complete the resume analysis first."
            )

    with tab10:
        st.markdown("### 📑 Resume Section Detector")
        section_analysis = detect_resume_sections(resume_text)

        st.markdown("**Sections Found:**")
        col1, col2 = st.columns(2)

        with col1:
            if section_analysis["sections_found"]["experience"]:
                st.success("✅ Experience")
            else:
                st.error("❌ Experience")

            if section_analysis["sections_found"]["education"]:
                st.success("✅ Education")
            else:
                st.error("❌ Education")

            if section_analysis["sections_found"]["skills"]:
                st.success("✅ Skills")
            else:
                st.error("❌ Skills")

        with col2:
            if section_analysis["sections_found"]["summary"]:
                st.success("✅ Summary/Objective")
            else:
                st.info("○ Summary/Objective (optional)")

            if section_analysis["sections_found"]["projects"]:
                st.success("✅ Projects")
            else:
                st.info("○ Projects (optional)")

            if section_analysis["sections_found"]["certifications"]:
                st.success("✅ Certifications")
            else:
                st.info("○ Certifications (optional)")

        if section_analysis["status"] == "success":
            st.success(f"✅ {section_analysis['recommendation']}")
        else:
            st.warning(f"⚠️ {section_analysis['recommendation']}")

    with tab11:
        st.markdown("### 📅 Date Format Checker")
        date_analysis = check_date_formats(resume_text)

        if date_analysis["formats_found"]:
            st.markdown("**Date Formats Detected:**")
            for format_name, count in date_analysis["formats_found"].items():
                st.markdown(f"• **{format_name}**: {count} instances")
        else:
            st.warning("No dates found in resume")

        if date_analysis["status"] == "success":
            st.success(f"✅ {date_analysis['recommendation']}")
        else:
            st.warning(f"⚠️ {date_analysis['recommendation']}")

        with st.expander("📌 Date Format Best Practices"):
            st.markdown("""
            **Recommended formats:**
            - Month YYYY (e.g., "January 2023")
            - Mon YYYY (e.g., "Jan 2023")
            
            **Tips:**
            - Be consistent throughout your resume
            - Use the same format for all dates
            - Consider using "Present" for current positions
            """)

    with tab12:
        st.markdown("### 🔄 Duplicate Content Finder")
        duplicate_analysis = find_duplicate_content(resume_text)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Duplicate Sentences", duplicate_analysis["duplicate_sentences"])
        with col2:
            st.metric("Repeated Phrases", duplicate_analysis["repeated_phrases"])

        if duplicate_analysis["status"] == "success":
            st.success(f"✅ {duplicate_analysis['recommendation']}")
        else:
            st.warning(f"⚠️ {duplicate_analysis['recommendation']}")

        if duplicate_analysis["duplicates"]:
            with st.expander("🔍 Duplicate Sentences Found"):
                for sentence, count in duplicate_analysis["duplicates"]:
                    st.warning(f"**Repeated {count} times:** {sentence[:100]}...")

        if duplicate_analysis["phrases"]:
            with st.expander("🔍 Repeated Phrases Found"):
                for phrase, count in duplicate_analysis["phrases"]:
                    st.info(f"**{count}x:** {phrase}")

    with tab13:
        st.markdown("### 🤖 ATS Format Validator")

        if pdf_path:
            ats_analysis = validate_ats_format(pdf_path)

            # ATS Score
            score = ats_analysis["ats_score"]
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if score >= 80:
                    st.success(f"### ✅ ATS Score: {score}/100")
                elif score >= 60:
                    st.warning(f"### ⚠️ ATS Score: {score}/100")
                else:
                    st.error(f"### ❌ ATS Score: {score}/100")
                st.markdown(f"**{ats_analysis['overall']}**")

            with col2:
                st.metric("Font Count", ats_analysis["font_count"])
            with col3:
                st.metric("Issues Found", len(ats_analysis["issues"]))

            # Metadata
            if ats_analysis["metadata"]:
                with st.expander("📄 PDF Metadata"):
                    for key, value in ats_analysis["metadata"].items():
                        st.markdown(f"**{key.title()}:** {value}")

            # Issues
            if ats_analysis["issues"]:
                st.markdown("**❌ Critical Issues:**")
                for issue in ats_analysis["issues"]:
                    st.error(f"• {issue}")
            else:
                st.success("✅ No critical issues found")

            # Warnings
            if ats_analysis["warnings"]:
                with st.expander(f"⚠️ Warnings ({len(ats_analysis['warnings'])})"):
                    for warning in ats_analysis["warnings"]:
                        st.warning(f"• {warning}")

            # Format checks
            st.markdown("**Format Checklist:**")
            col1, col2 = st.columns(2)
            with col1:
                if not ats_analysis["has_tables"]:
                    st.success("✅ No tables")
                else:
                    st.error("❌ Contains tables")

                if not ats_analysis["has_headers_footers"]:
                    st.success("✅ No headers/footers")
                else:
                    st.error("❌ Has headers/footers")

            with col2:
                if not ats_analysis["has_images"]:
                    st.success("✅ No images")
                else:
                    st.warning("⚠️ Contains images")

                if ats_analysis["font_count"] <= 2:
                    st.success(f"✅ {ats_analysis['font_count']} font(s)")
                else:
                    st.warning(f"⚠️ {ats_analysis['font_count']} fonts (recommend ≤2)")

            # Best practices
            with st.expander("📚 ATS Best Practices"):
                st.markdown("""
                **For best ATS compatibility:**
                - ✅ Use simple, single-column layout
                - ✅ Stick to standard fonts (Arial, Calibri, Times New Roman)
                - ✅ Avoid tables, text boxes, and headers/footers
                - ✅ Save as text-based PDF (not scanned)
                - ✅ Use standard section headings
                - ✅ Keep formatting simple and clean
                """)
        else:
            st.info(
                "ATS validation requires PDF file. Upload and analyze to see results."
            )

    with tab14:
        st.markdown("### 📧 Email Analysis Results")

        # Always update analysis in session state when available
        if analysis_result:
            st.session_state["email_analysis"] = analysis_result
            if st.session_state.analysis_history:
                st.session_state["email_filename"] = st.session_state.analysis_history[
                    -1
                ].get("filename", "resume")

        # Check SMTP
        smtp_email = os.getenv("SMTP_EMAIL", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")

        if not smtp_email or not smtp_password:
            st.warning("⚠️ Email not configured")
            return

        st.success(f"✅ Ready: {smtp_email}")

        # Check if we have analysis
        if "email_analysis" not in st.session_state:
            st.info("📊 Analyze a resume first")
            return

        st.divider()

        # Initialize send state
        if "email_send_result" not in st.session_state:
            st.session_state["email_send_result"] = None

        # Email input
        recipient = st.text_input(
            "📧 Recipient Email",
            key=f"email_recipient{key_suffix}",
            placeholder="example@email.com",
        )

        # Send button with callback
        def send_email_callback():
            recipient_email = st.session_state.get(f"email_recipient{key_suffix}", "")
            if not recipient_email:
                st.session_state["email_send_result"] = ("error", "Please enter email")
            elif "@" not in recipient_email:
                st.session_state["email_send_result"] = ("error", "Invalid email")
            else:
                try:
                    # Generate PDF
                    pdf_buffer = create_analysis_report(
                        st.session_state["email_analysis"],
                        st.session_state.get("email_filename", "resume"),
                    )
                    pdf_bytes = pdf_buffer.getvalue()

                    # Send email
                    result = send_analysis_email(
                        recipient_email,
                        st.session_state["email_analysis"],
                        pdf_bytes,
                        st.session_state.get("email_filename", "resume"),
                    )

                    if result["success"]:
                        st.session_state["email_send_result"] = (
                            "success",
                            f"Email sent to {recipient_email}!",
                        )
                    else:
                        st.session_state["email_send_result"] = (
                            "error",
                            result["error"],
                        )
                except Exception as e:
                    st.session_state["email_send_result"] = ("error", str(e))

        st.button(
            "📤 SEND EMAIL NOW",
            key=f"send_btn{key_suffix}",
            type="primary",
            use_container_width=True,
            on_click=send_email_callback,
        )

        # Show result
        if st.session_state["email_send_result"]:
            result_type, result_msg = st.session_state["email_send_result"]
            if result_type == "success":
                st.success(f"✅ {result_msg}")
                st.balloons()
            else:
                st.error(f"❌ {result_msg}")

    add_vertical_space(2)

    add_vertical_space(2)


def sidebar_content():
    """Create sidebar content"""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")

        # AI Provider Selection
        st.markdown("### 🤖 AI Provider")
        ai_provider = st.selectbox(
            "Choose AI Provider",
            ["groq", "gemini"],
            index=0 if os.getenv("AI_PROVIDER", "groq") == "groq" else 1,
            help="Groq is recommended for better free tier (faster, higher limits)",
        )
        st.session_state.ai_provider = ai_provider

        # API Key Input
        if ai_provider == "groq":
            st.markdown("### 🔑 Groq API Key")
            api_key_default = os.getenv("GROQ_API_KEY", "")
            api_key_help = "Get your free API key from https://console.groq.com/keys"
        else:
            st.markdown("### 🔑 Gemini API Key")
            api_key_default = os.getenv("GEMINI_API_KEY", "")
            api_key_help = (
                "Get your free API key from https://makersuite.google.com/app/apikey"
            )

        api_key = st.text_input(
            f"Enter your {ai_provider.title()} API Key",
            type="password",
            value=api_key_default,
            help=api_key_help,
        )

        if api_key:
            st.session_state.api_key = api_key

        st.markdown("---")

        # Tips & Resources
        st.markdown("### 💡 Resume Tips")
        with st.expander("📌 Quick Tips"):
            st.markdown("""
            - **Use keywords** from the job description
            - **Quantify achievements** with numbers
            - **Keep it concise** (1-2 pages max)
            - **Use action verbs** (Led, Managed, Created)
            - **Tailor for each application**
            - **Include relevant skills** prominently
            """)

        with st.expander("🎯 ATS Guidelines"):
            st.markdown("""
            - Use **standard section headings**
            - Avoid **images, tables, and graphics**
            - Use **standard fonts** (Arial, Calibri)
            - Save as **.docx or .pdf**
            - **Don't use headers/footers**
            - Include **full contact information**
            """)

        with st.expander("🔗 Helpful Resources"):
            st.markdown("""
            - [Resume Templates](https://www.resume.io/resume-templates)
            - [Action Verbs List](https://www.indeed.com/career-advice/resumes-cover-letters/action-verbs-to-make-your-resume-stand-out)
            - [Get Groq API Key](https://console.groq.com/keys) (Recommended)
            - [Get Gemini API Key](https://makersuite.google.com/app/apikey)
            """)

        st.markdown("---")

        # History
        if "analysis_history" in st.session_state and st.session_state.analysis_history:
            st.markdown("### 📜 Recent Analyses")
            for i, hist in enumerate(
                reversed(st.session_state.analysis_history[-3:]), 1
            ):
                with st.expander(f"{i}. {hist['filename'][:20]}..."):
                    st.write(f"**Score:** {hist['score']}%")
                    st.write(f"**Date:** {hist['date']}")

        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; font-size: 0.8rem; opacity: 0.7;">
                Built with ❤️ using Streamlit<br/>
                Powered by Google Gemini AI
            </div>
        """,
            unsafe_allow_html=True,
        )


def main():
    """Main application function"""

    # Load custom CSS
    load_custom_css()

    # Initialize session state
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []

    # Sidebar
    sidebar_content()

    # Hero Section
    create_hero_section()

    # How It Works
    create_how_it_works()

    # Main Content
    st.markdown("## 📤 Upload Resume & Job Description")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📄 Upload Your Resume(s)")

        # Multi-file upload option
        upload_mode = st.radio(
            "Upload mode:",
            ["Single Resume", "Multiple Resumes (up to 3)"],
            horizontal=True,
        )

        if upload_mode == "Single Resume":
            uploaded_file = st.file_uploader(
                "Choose a PDF file",
                type=["pdf"],
                help="Upload your resume in PDF format (max 5MB)",
            )
            uploaded_files = [uploaded_file] if uploaded_file else []
        else:
            uploaded_files_raw = st.file_uploader(
                "Choose PDF files",
                type=["pdf"],
                accept_multiple_files=True,
                help="Upload 2-3 resumes in PDF format for comparison",
            )
            uploaded_files = uploaded_files_raw[:3] if uploaded_files_raw else []
            if len(uploaded_files_raw) > 3:
                st.warning(
                    "⚠️ Maximum 3 resumes allowed. Only first 3 will be analyzed."
                )

        # Display uploaded files
        if uploaded_files:
            for idx, uploaded_file in enumerate(uploaded_files, 1):
                # Validate file
                is_valid, error_msg = validate_pdf(uploaded_file)

                if not is_valid:
                    st.error(f"❌ File {idx}: {error_msg}")
                else:
                    file_info = get_file_info(uploaded_file)
                    st.success(
                        f"✅ **Resume {idx}**: {file_info['name']} ({file_info['size_mb']} MB)"
                    )

                    # Extract text preview
                    with st.expander(f"👁️ Preview Resume {idx}"):
                        resume_text = extract_text_from_pdf(uploaded_file)
                        if resume_text:
                            st.text_area(
                                f"Resume {idx} Content",
                                resume_text[:500] + "...",
                                height=200,
                                disabled=True,
                                key=f"preview_{idx}",
                            )
                        else:
                            st.error("Could not extract text from PDF")

    with col2:
        st.markdown("### 📝 Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=300,
            placeholder="Copy and paste the full job description, including requirements, responsibilities, and qualifications...",
            help="Include as much detail as possible for better analysis",
        )

        if job_description:
            word_count = len(job_description.split())
            st.info(f"📊 Word count: {word_count}")

    add_vertical_space(2)

    # Analyze Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🚀 Analyze Resume(s)", width="stretch")

    # Analysis
    if analyze_button:
        # Validation
        if not uploaded_files:
            st.error("❌ Please upload at least one resume PDF file")
            return

        if not job_description or len(job_description.strip()) < 50:
            st.error(
                "❌ Please provide a detailed job description (at least 50 characters)"
            )
            return

        if "api_key" not in st.session_state or not st.session_state.api_key:
            st.error("❌ Please enter your Gemini API key in the sidebar")
            return

        # Process each resume
        all_results = []

        for idx, uploaded_file in enumerate(uploaded_files, 1):
            st.markdown("---")
            st.markdown(f"## 📊 Analysis Results - Resume {idx}: {uploaded_file.name}")

            # Extract resume text
            with st.spinner(f"📄 Extracting text from resume {idx}..."):
                resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text:
                st.error(
                    f"❌ Could not extract text from {uploaded_file.name}. Please ensure it's a text-based PDF."
                )
                continue

            # Perform analysis
            with st.spinner(
                f"🤖 Analyzing resume {idx} with AI... This may take 10-30 seconds..."
            ):
                # Get AI provider from session state or env
                ai_provider = st.session_state.get(
                    "ai_provider", os.getenv("AI_PROVIDER", "gemini")
                )

                if ai_provider == "groq":
                    analysis_result = analyze_resume_with_groq(
                        resume_text, job_description, st.session_state.api_key
                    )
                else:
                    analysis_result = analyze_resume_with_gemini(
                        resume_text, job_description, st.session_state.api_key
                    )

            if analysis_result:
                # Store uploaded file path temporarily for ATS validation
                import tempfile

                with tempfile.NamedTemporaryFile(
                    delete=False, suffix=".pdf"
                ) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name

                # Save to results
                all_results.append(
                    {
                        "filename": uploaded_file.name,
                        "analysis": analysis_result,
                        "text": resume_text,
                        "temp_path": tmp_path,
                    }
                )

                # Save to history
                st.session_state.analysis_history.append(
                    {
                        "filename": uploaded_file.name,
                        "score": analysis_result.get("match_score", 0),
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "result": analysis_result,
                    }
                )

                # Display results
                display_results(
                    analysis_result, uploaded_file.name, key_suffix=f"_{idx}"
                )

                # Display additional features (including ATS validation)
                display_additional_features(
                    resume_text, analysis_result, tmp_path, key_suffix=f"_{idx}"
                )

                # Clean up temp file
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

            else:
                st.error(
                    f"❌ Analysis failed for {uploaded_file.name}. Please check your API key."
                )

        # Comparison section for multiple resumes
        if len(all_results) > 1:
            st.markdown("---")
            st.markdown("## 📊 Resume Comparison")

            comparison_data = []
            for result in all_results:
                comparison_data.append(
                    {
                        "Resume": result["filename"],
                        "Match Score": f"{result['analysis'].get('match_score', 0)}%",
                        "Rating": result["analysis"].get("match_rating", "N/A"),
                        "Technical Skills": len(
                            result["analysis"]
                            .get("found_keywords", {})
                            .get("technical_skills", [])
                        ),
                        "Soft Skills": len(
                            result["analysis"]
                            .get("found_keywords", {})
                            .get("soft_skills", [])
                        ),
                        "Missing Critical": len(
                            result["analysis"]
                            .get("missing_keywords", {})
                            .get("critical_technical_skills", [])
                        ),
                    }
                )

            import pandas as pd

            df_comparison = pd.DataFrame(comparison_data)

            st.dataframe(df_comparison, width="stretch")

            # Best resume highlight - Smart selection based on multiple criteria
            def get_resume_score(idx):
                """Calculate composite score for resume selection"""
                analysis = all_results[idx]["analysis"]

                match_score = analysis.get("match_score", 0)
                tech_skills = len(
                    analysis.get("found_keywords", {}).get("technical_skills", [])
                )
                soft_skills = len(
                    analysis.get("found_keywords", {}).get("soft_skills", [])
                )
                missing_critical = len(
                    analysis.get("missing_keywords", {}).get(
                        "critical_technical_skills", []
                    )
                )

                # Return tuple for comparison: (match_score, tech_skills, soft_skills, -missing_critical)
                # Negative missing_critical so lower values rank higher
                return (match_score, tech_skills, soft_skills, -missing_critical)

            best_idx = max(range(len(all_results)), key=get_resume_score)

            best_analysis = all_results[best_idx]["analysis"]
            best_tech = len(
                best_analysis.get("found_keywords", {}).get("technical_skills", [])
            )
            best_soft = len(
                best_analysis.get("found_keywords", {}).get("soft_skills", [])
            )
            best_missing = len(
                best_analysis.get("missing_keywords", {}).get(
                    "critical_technical_skills", []
                )
            )

            st.success(
                f"🏆 **Best Match**: {all_results[best_idx]['filename']} - "
                f"{all_results[best_idx]['analysis'].get('match_score', 0)}% match "
                f"(Tech: {best_tech}, Soft: {best_soft}, Missing Critical: {best_missing})"
            )

        if all_results:
            st.balloons()
        else:
            st.error(
                "❌ Analysis failed. Please check your API key and try again. If the problem persists, you may have reached the API rate limit."
            )

    # Footer
    add_vertical_space(3)
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 2rem; color: #6b7280;">
            <p style="font-size: 0.9rem;">
                💡 <strong>Pro Tip:</strong> Run multiple analyses with different job descriptions to optimize your resume for various positions!
            </p>
            <p style="font-size: 0.8rem; margin-top: 1rem;">
                This tool uses AI for analysis. Always review and validate the suggestions before making changes to your resume.
            </p>
        </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
