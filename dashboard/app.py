import streamlit as st
import pandas as pd
import plotly.express as px
import os
import subprocess
import shutil

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="GradeAI Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main{
    background-color:#F8FAFC;
}

.block-container{
    padding-top:1rem;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:15px;
    border-left:5px solid #4F46E5;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

.top-banner{
    background:linear-gradient(
        90deg,
        #4F46E5,
        #7C3AED
    );
    
    padding:25px;
    border-radius:15px;
    color:white;
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# PATHS
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

csv_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "master_performance.csv"
)

feedback_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "student_feedback.csv"
)

email_status_path = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "email_status.csv"
)

logo_path = os.path.join(
    BASE_DIR,
    "assets",
    "logo.webp"
)

# ==================================================
# LOAD DATA
# ==================================================

df = pd.read_csv(csv_path)

feedback_df = pd.read_csv(feedback_path)

# ==================================================
# SIDEBAR
# ==================================================

if os.path.exists(logo_path):
    st.sidebar.image(
        logo_path,
        width=180
    )

st.sidebar.title("🎓 GradeAI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Student Analytics",
        "Leaderboard",
        "AI Insights",
        "Upload Portal",
        "Reports",
        "Email Status"
    ]
)

# ==================================================
# HEADER
# ==================================================

st.title("🎓 GradeAI Dashboard")

st.markdown("""
<div class="top-banner">

<h2>🚀 GradeAI Performance Management System</h2>

<p>
AI Powered Academic Analytics Platform
</p>

</div>
""", unsafe_allow_html=True)

# ==================================================
# KPI CARDS
# ==================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "👨‍🎓 Students",
        len(df)
    )

with c2:
    st.metric(
        "📊 Average %",
        round(
            df["Percentage"].mean(),
            2
        )
    )

with c3:
    st.metric(
        "🏆 Top Score",
        df["Total Marks"].max()
    )

with c4:
    st.metric(
        "🎯 Avg Percentile",
        round(
            df["Percentile"].mean(),
            2
        )
    )

st.divider()

# ==================================================
# OVERVIEW
# ==================================================

if page == "Overview":

    topper = df.sort_values(
        "Rank"
    ).iloc[0]

    st.success(
        f"""
🏆 Top Performer

Email: {topper['Email']}

Rank: #{topper['Rank']}

Grade: {topper['Grade']}

Percentage: {topper['Percentage']:.2f}%
"""
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            df,
            names="Grade",
            title="Grade Distribution",
            hole=0.5
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.histogram(
            df,
            x="Percentage",
            title="Percentage Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Class Performance")

    fig = px.bar(
        df.sort_values(
            "Rank"
        ).head(10),
        x="Email",
        y="Percentage",
        color="Grade",
        title="Top 10 Students"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# STUDENT ANALYTICS
# ==================================================

elif page == "Student Analytics":

    email = st.selectbox(
        "Select Student",
        df["Email"].unique()
    )

    student = df[
        df["Email"] == email
    ]

    st.subheader(
        "👤 Student Profile"
    )

    st.dataframe(
        student,
        use_container_width=True
    )

    feedback = feedback_df[
        feedback_df["Email"] == email
    ]

    if not feedback.empty:

        st.subheader(
            "🤖 AI Feedback"
        )

        st.info(
            feedback.iloc[0][
                "AI_Feedback"
            ]
        )

    quiz_cols = [
        col
        for col in df.columns
        if col.startswith(
            "Quiz_"
        )
    ]

    if len(quiz_cols) > 0:

        chart_df = pd.DataFrame({
            "Quiz": quiz_cols,
            "Marks": [
                student.iloc[0][col]
                for col in quiz_cols
            ]
        })

        fig = px.line(
            chart_df,
            x="Quiz",
            y="Marks",
            markers=True,
            title="Quiz Performance Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==================================================
# LEADERBOARD
# ==================================================

elif page == "Leaderboard":

    st.header(
        "🏆 Leaderboard"
    )

    leaderboard = df.sort_values(
        "Rank"
    )

    st.dataframe(
        leaderboard[
            [
                "Rank",
                "Email",
                "Total Marks",
                "Percentage",
                "Grade"
            ]
        ],
        use_container_width=True
    )

    fig = px.bar(
        leaderboard.head(10),
        x="Email",
        y="Total Marks",
        color="Grade",
        title="Top 10 Students"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==================================================
# AI INSIGHTS
# ==================================================

elif page == "AI Insights":

    st.header(
        "🤖 AI Insights"
    )

    avg_percentage = round(
        df["Percentage"].mean(),
        2
    )

    top_grade = df[
        "Grade"
    ].value_counts().idxmax()

    risk_students = len(
        df[
            df["Grade"].isin(
                ["D", "F"]
            )
        ]
    )

    top_student = df.sort_values(
        "Rank"
    ).iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Average %",
            avg_percentage
        )

    with c2:
        st.metric(
            "Most Common Grade",
            top_grade
        )

    with c3:
        st.metric(
            "Students At Risk",
            risk_students
        )

    st.success(
        f"""
🏆 Top Student

Email: {top_student['Email']}

Percentage: {top_student['Percentage']:.2f}%

Grade: {top_student['Grade']}
"""
    )

    if avg_percentage < 60:

        st.error(
            """
Class performance needs improvement.

Recommendation:
Conduct revision sessions.
"""
        )

    elif avg_percentage < 75:

        st.warning(
            """
Class performance is average.

Recommendation:
Provide extra practice quizzes.
"""
        )

    else:

        st.success(
            """
Class is performing very well.

Recommendation:
Maintain current learning strategy.
"""
        )

# ==================================================
# UPLOAD PORTAL
# ==================================================

elif page == "Upload Portal":

    st.header("📂 Upload Quiz Files")

    st.info(
        """
Upload one or more quiz CSV files.

Example:
Quiz1.csv
Quiz2.csv
Quiz3.csv
"""
    )

    uploaded_files = st.file_uploader(
        "Choose CSV Files",
        type=["csv"],
        accept_multiple_files=True
    )

    quiz_folder = os.path.join(
        BASE_DIR,
        "data",
        "quizzes"
    )

    os.makedirs(
        quiz_folder,
        exist_ok=True
    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} file(s) selected"
        )

        for file in uploaded_files:

            st.write(
                f"📄 {file.name}"
            )

    if st.button(
        "🚀 Process Uploaded Files"
    ):

        if not uploaded_files:

            st.warning(
                "Please upload at least one CSV file."
            )

        else:

            try:

                for file in uploaded_files:

                    save_path = os.path.join(
                        quiz_folder,
                        file.name
                    )

                    with open(
                        save_path,
                        "wb"
                    ) as f:

                        f.write(
                            file.getbuffer()
                        )

                st.success(
                    "Files uploaded successfully."
                )

                st.info(
                    "Running GradeAI..."
                )

                result = subprocess.run(
                    ["python", "process_only.py"],
                    capture_output=True,
                    text=True,
                    cwd=BASE_DIR
                )

                if result.returncode == 0:

                    st.success(
                        """
Processing Complete.

Refresh dashboard pages to view updated analytics.
"""
                    )

                else:

                    st.error(
                        result.stderr
                    )

            except Exception as e:

                st.error(str(e))

# ==================================================
# REPORTS
# ==================================================

elif page == "Reports":

    st.header(
        "📄 Reports"
    )

    csv = df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download Master Report",
        data=csv,
        file_name="master_performance.csv",
        mime="text/csv"
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# ==================================================
# EMAIL STATUS
# ==================================================

elif page == "Email Status":

    st.header(
        "📧 Email Status"
    )

    if os.path.exists(
        email_status_path
    ):

        email_df = pd.read_csv(
            email_status_path
        )

        st.dataframe(
            email_df,
            use_container_width=True
        )

        sent = len(
            email_df[
                email_df["Status"]
                == "Sent"
            ]
        )

        failed = len(
            email_df[
                email_df["Status"]
                == "Failed"
            ]
        )

        c1, c2 = st.columns(2)

        with c1:
            st.metric(
                "Emails Sent",
                sent
            )

        with c2:
            st.metric(
                "Emails Failed",
                failed
            )

        fig = px.pie(
            email_df,
            names="Status",
            title="Email Delivery Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "🎓 GradeAI | Lloyd Institute of Engineering & Technology"
)