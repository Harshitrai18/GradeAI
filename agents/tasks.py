from crewai import Task

analysis_task=Task(
    description="Analyze scores"
)

grade_task=Task(
    description="Assign grades"
)

report_task=Task(
    description="Generate reports"
)