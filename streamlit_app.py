import os
import threading

import streamlit as st
from dotenv import load_dotenv


# --------------------------------
# Load environment variables
# --------------------------------

load_dotenv()


# --------------------------------
# Load Streamlit secrets
# --------------------------------

try:

    if "OPENAI_API_KEY" in st.secrets:

        os.environ["OPENAI_API_KEY"] = (
            st.secrets["OPENAI_API_KEY"]
        )

except Exception:
    pass


# --------------------------------
# Project imports
# --------------------------------

from flow import SoftwareDevelopmentFlow

from status import (
    start_project,
    get_status
)

from database import (
    get_recent_projects
)


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="AI Software Development Team",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------
# Authentication
# --------------------------------

def check_password():

    try:
        app_password = st.secrets["APP_PASSWORD"]

    except Exception:

        app_password = os.getenv(
            "APP_PASSWORD"
        )

    if not app_password:

        return True

    if "authenticated" not in st.session_state:

        st.session_state.authenticated = False

    if st.session_state.authenticated:

        return True

    st.title("🔐 AI Software Development Team")

    password = st.text_input(
        "Enter application password",
        type="password"
    )

    if st.button("Login"):

        if password == app_password:

            st.session_state.authenticated = True

            st.rerun()

        else:

            st.error(
                "Incorrect password."
            )

    return False


if not check_password():

    st.stop()


# --------------------------------
# Header
# --------------------------------

st.title(
    "🤖 AI Software Development Team"
)

st.write(
    "Build software with a team of specialized AI agents."
)


# --------------------------------
# Project input
# --------------------------------

project_idea = st.text_area(
    "What do you want to build?",
    placeholder=(
        "Example: Build an online bookstore"
    ),
    height=120
)


# --------------------------------
# Start project
# --------------------------------

if st.button(
    "🚀 Start AI Team",
    type="primary"
):

    project_idea = project_idea.strip()

    if not project_idea:

        st.error(
            "Project idea cannot be empty."
        )

    else:

        current = get_status()

        if current["project"]["state"] == "running":

            st.warning(
                "A project is already running."
            )

        else:

            start_project(
                project_idea
            )

            def run_project():

                try:

                    flow = SoftwareDevelopmentFlow()

                    flow.state.project_idea = (
                        project_idea
                    )

                    flow.kickoff()

                except Exception as error:

                    from status import fail_project

                    fail_project(error)


            thread = threading.Thread(
                target=run_project,
                daemon=True
            )

            thread.start()

            st.session_state.project_started = True

            st.success(
                "AI team started!"
            )


# --------------------------------
# Live status dashboard
# --------------------------------

st.divider()

st.subheader(
    "📊 Team Status"
)


@st.fragment(run_every=1)
def live_status():

    current_status = get_status()

    agents = current_status["agents"]

    columns = st.columns(4)

    for column, (agent, state) in zip(
        columns,
        agents.items()
    ):

        with column:

            if state == "working":

                st.info(
                    f"🔄 {agent}\n\nWORKING"
                )

            elif state == "completed":

                st.success(
                    f"✅ {agent}\n\nCOMPLETED"
                )

            else:

                st.warning(
                    f"⏳ {agent}\n\nWAITING"
                )


    project = current_status["project"]

    st.write(
        "**Project:**",
        project["project_idea"]
    )

    st.write(
        "**Status:**",
        project["state"]
    )


    if project["state"] == "completed":

        st.success(
            "🎉 Project completed!"
        )

        st.subheader(
            "Final Result"
        )

        st.write(
            project["result"]
        )


    elif project["state"] == "error":

        st.error(
            "❌ Project failed"
        )

        st.code(
            project["error"]
        )


live_status()


# --------------------------------
# Project history
# --------------------------------

st.divider()

st.subheader(
    "📚 Project History"
)


history = get_recent_projects()


if history:

    for project in history:

        with st.expander(
            f"#{project['id']} — "
            f"{project['project_idea']}"
        ):

            st.write(
                "Status:",
                project["state"]
            )

            st.write(
                "Created:",
                project["created_at"]
            )

            if project["result"]:

                st.write(
                    "Result:",
                    project["result"]
                )

            if project["error"]:

                st.error(
                    project["error"]
                )

else:

    st.info(
        "No project history yet."
    )