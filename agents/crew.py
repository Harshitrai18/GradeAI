from crewai import Crew
from agents.agents import *

crew=Crew(
    agents=[
        performance_agent,
        grade_agent,
        report_agent
    ]
)