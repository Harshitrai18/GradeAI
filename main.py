import os
import pandas as pd

from services.data_merger import merge_quizzes
from services.performance import calculate_performance
from services.grade_calculator import assign_grade
from services.feedback import get_ai_feedback
from services.report_agent import report_agent
from services.email_agent import email_agent

# ==================================
# CREATE REQUIRED FOLDERS
# ==================================

os.makedirs("data/processed", exist_ok=True)
os.makedirs("gradecards", exist_ok=True)

print("Starting GradeAI Processing...")

# ==================================
# MERGE QUIZZES
# ==================================

print("Merging Quiz Files...")

df = merge_quizzes()

# ==================================
# CALCULATE PERFORMANCE
# ==================================

print("Calculating Performance...")

df = calculate_performance(df)

# ==================================
# ASSIGN GRADE
# ==================================

print("Assigning Grades...")

df["Grade"] = df["Percentage"].apply(
    assign_grade
)

# ==================================
# AI FEEDBACK
# ==================================

print("Generating AI Feedback...")

feedback_list = []

for _, student in df.iterrows():

    feedback = get_ai_feedback(student)

    feedback_list.append(feedback)

df["AI_Feedback"] = feedback_list

# ==================================
# SAVE MASTER REPORT
# ==================================

master_csv = "data/processed/master_performance.csv"

df.to_csv(
    master_csv,
    index=False
)

print("Master Report Saved")

# ==================================
# GENERATE PDF + SEND EMAIL
# ==================================

email_status = []

for _, student in df.iterrows():

    print(f"Processing {student['Email']}")

    pdf_path = report_agent(student)

    status = email_agent(
        student,
        pdf_path
    )

    email_status.append(
        {
            "Email": student["Email"],
            "Status": "Sent" if status else "Failed"
        }
    )

# ==================================
# SAVE EMAIL STATUS
# ==================================

status_df = pd.DataFrame(
    email_status
)

status_df.to_csv(
    "data/processed/email_status.csv",
    index=False
)

# ==================================
# SAVE FEEDBACK FILE
# ==================================

df[
    [
        "Email",
        "Grade",
        "Rank",
        "AI_Feedback"
    ]
].to_csv(
    "data/processed/student_feedback.csv",
    index=False
)

# ==================================
# SUMMARY
# ==================================

print("\nProcessing Complete")

print("=" * 50)

print(f"Students Processed : {len(df)}")

print(
    f"Average Percentage : "
    f"{round(df['Percentage'].mean(),2)}"
)

print(
    f"Top Score : "
    f"{df['Total Marks'].max()}"
)

print("=" * 50)

print("GradeAI Finished Successfully")