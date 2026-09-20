from crewai import Agent, Task, Crew
from tools import project_info, search_project_knowledge
from status import task_completed


# ==================================================
# 1. PRODUCT MANAGER
# ==================================================

product_manager = Agent(
    role="Product Manager",

    goal="Understand the user's software idea and create clear requirements.",

    backstory="""
    You are an experienced product manager.
    You understand user needs and turn software ideas
    into clear and useful requirements.
    """,

    verbose=True
)


# ==================================================
# 2. SOFTWARE ARCHITECT
# ==================================================

architect = Agent(
    role="Software Architect",

    goal="Design a clear and scalable architecture for the software project.",

    backstory="""
    You are an experienced software architect.
    You design APIs, databases, application structure,
    and technical solutions.
    """,

    verbose=True
)


# ==================================================
# 3. SOFTWARE DEVELOPER
# ==================================================

developer = Agent(
    role="Senior Software Developer",

    goal="Implement software based on the requirements and architecture.",

    backstory="""
    You are an experienced software developer.

    You write clean, readable, maintainable,
    and reliable code.

    You follow the requirements and architecture
    created by the other team members.

    Before implementing the software, use the
    project knowledge search tool when you need
    information about project standards or guidelines.
    """,

    tools=[
        project_info,
        search_project_knowledge
    ],

    verbose=True
)


# ==================================================
# 4. QA ENGINEER
# ==================================================

qa_engineer = Agent(
    role="QA Engineer",

    goal="Test the software and identify bugs and missing requirements.",

    backstory="""
    You are an experienced QA engineer.

    You carefully test software.

    You look for:

    - Bugs
    - Missing functionality
    - Incorrect behavior
    - Requirement violations
    - Possible improvements
    """,

    verbose=True
)


# ==================================================
# 5. REQUIREMENTS TASK
# ==================================================

requirements_task = Task(
    description="""
    Analyze this software project:

    {project_idea}

    Identify:

    1. Main users
    2. Main features
    3. Functional requirements
    4. Non-functional requirements
    5. Important questions
    """,

    expected_output="""
    A clear software requirements document containing:

    - Main users
    - Main features
    - Functional requirements
    - Non-functional requirements
    - Important questions
    """,

    agent=product_manager
)


# ==================================================
# 6. ARCHITECTURE TASK
# ==================================================

architecture_task = Task(
    description="""
    Design the technical architecture for the software project.

    Use the requirements created by the Product Manager.

    Explain:

    1. Frontend
    2. Backend
    3. Database
    4. API structure
    5. Main components
    6. How the components communicate
    """,

    expected_output="""
    A clear technical architecture document
    explaining the frontend, backend, database,
    APIs, and main application components.
    """,

    agent=architect,

    context=[
        requirements_task
    ]
)


# ==================================================
# 7. DEVELOPMENT TASK
# ==================================================

development_task = Task(
    description="""
    Implement a simple version of the software project.

    Use the requirements and architecture provided
    by the previous team members.

    Before implementing the software, search the
    project knowledge base for relevant coding
    standards and guidelines.

    Follow the relevant standards you find.

    Create clean and readable Python code.

    Explain the important parts of the implementation.
    """,

    expected_output="""
    Python implementation of the application
    together with a clear explanation of the code
    and how the project knowledge was used.
    """,

    agent=developer,

    context=[
        requirements_task,
        architecture_task
    ]
)


# ==================================================
# 8. TESTING TASK
# ==================================================

testing_task = Task(
    description="""
    Review the software implementation.

    Compare the implementation with:

    1. The original requirements
    2. The proposed architecture

    Look for:

    - Bugs
    - Missing features
    - Incorrect behavior
    - Architecture problems
    - Potential improvements

    Create a clear QA report.
    """,

    expected_output="""
    A QA report containing:

    - Problems found
    - Missing requirements
    - Potential bugs
    - Architecture issues
    - Suggested improvements
    """,

    agent=qa_engineer,

    context=[
        requirements_task,
        architecture_task,
        development_task
    ]
)


# ==================================================
# 9. CREATE THE CREW
# ==================================================

crew = Crew(

    agents=[
        product_manager,
        architect,
        developer,
        qa_engineer
    ],

    tasks=[
        requirements_task,
        architecture_task,
        development_task,
        testing_task
    ],

    verbose=True,

    # Update dashboard whenever a task finishes
    task_callback=lambda output: task_completed()
)


# ==================================================
# 10. RUN CREW ONLY WHEN main.py IS DIRECTLY RUN
# ==================================================

if __name__ == "__main__":

    result = crew.kickoff(
        inputs={
            "project_idea": "Build an online bookstore"
        }
    )

    print("\n")
    print("=" * 60)
    print("AI SOFTWARE DEVELOPMENT TEAM - FINAL RESULT")
    print("=" * 60)
    print("\n")

    print(result)