import pandas as pd

from services.data_merger import merge_quizzes
from services.performance import calculate_performance
from services.grade_calculator import assign_grade
from services.feedback import get_ai_feedback
from services.report_agent import report_agent

print("Processing Files...")

df = merge_quizzes()

df = calculate_performance(df)

df["Grade"] = df["Percentage"].apply(
    assign_grade
)

feedback_list = []

for _, student in df.iterrows():

    feedback = get_ai_feedback(student)

    feedback_list.append(feedback)

df["AI_Feedback"] = feedback_list

df.to_csv(
    "data/processed/master_performance.csv",
    index=False
)

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

for _, student in df.iterrows():

    report_agent(student)

print("Done")