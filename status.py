from threading import Lock

from database import (
    create_project,
    update_project
)


AGENTS = [
    "Product Manager",
    "Software Architect",
    "Developer",
    "QA Engineer"
]


agent_status = {
    agent: "waiting"
    for agent in AGENTS
}


project_status = {
    "id": None,
    "state": "idle",
    "project_idea": "",
    "result": "",
    "error": ""
}


current_agent_index = 0

lock = Lock()


def start_project(project_idea):

    global current_agent_index

    project_id = create_project(project_idea)

    with lock:

        current_agent_index = 0

        for agent in AGENTS:
            agent_status[agent] = "waiting"

        agent_status["Product Manager"] = "working"

        project_status["id"] = project_id
        project_status["state"] = "running"
        project_status["project_idea"] = project_idea
        project_status["result"] = ""
        project_status["error"] = ""


def task_completed():

    global current_agent_index

    with lock:

        if current_agent_index >= len(AGENTS):
            return

        current_agent = AGENTS[current_agent_index]

        agent_status[current_agent] = "completed"

        current_agent_index += 1

        if current_agent_index < len(AGENTS):

            next_agent = AGENTS[current_agent_index]

            agent_status[next_agent] = "working"


def complete_project(result):

    with lock:

        project_status["state"] = "completed"
        project_status["result"] = str(result)

        project_id = project_status["id"]

    if project_id:

        update_project(
            project_id,
            "completed",
            result=result
        )


def fail_project(error):

    with lock:

        project_status["state"] = "error"
        project_status["error"] = str(error)

        project_id = project_status["id"]

    if project_id:

        update_project(
            project_id,
            "error",
            error=error
        )


def get_status():

    with lock:

        return {
            "agents": agent_status.copy(),
            "project": project_status.copy()
        }