from crewai import Agent

performance_agent=Agent(
    role="Performance Analyst",
    goal="Analyze student performance",
    backstory="Expert trainer"
)

grade_agent=Agent(
    role="Grade Generator",
    goal="Generate grades"
)

report_agent=Agent(
    role="Report Generator",
    goal="Generate grade cards"
)