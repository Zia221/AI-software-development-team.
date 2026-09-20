import os
import threading
import hashlib
import hmac
import secrets


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
        str(st.secrets["OPENAI_API_KEY"]).strip()
    )
  elif os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = (
        os.getenv("OPENAI_API_KEY").strip()
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

from status import fail_project

from database import (
    get_recent_projects,
    create_user,
    get_user
)


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="AI Software Development Team",
    page_icon="🤖",
    layout="wide"
)


# =================================
# PASSWORD SECURITY
# =================================

def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000
    )

    return (
        salt.hex()
        + ":"
        + password_hash.hex()
    )


def verify_password(
    password,
    stored_password
):

    try:

        salt_hex, hash_hex = (
            stored_password.split(":")
        )

        salt = bytes.fromhex(
            salt_hex
        )

        stored_hash = bytes.fromhex(
            hash_hex
        )

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            100_000
        )

        return hmac.compare_digest(
            password_hash,
            stored_hash
        )

    except Exception:

        return False


# =================================
# AUTHENTICATION
# =================================

def authentication_page():

    st.title(
        "🤖 AI Software Development Team"
    )

    # --------------------------------
    # Login / Register tabs
    # --------------------------------

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )

    # =================================
    # LOGIN
    # =================================

    with login_tab:

        st.subheader(
            "Login"
        )

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            type="primary",
            key="login_button"
        ):

            username = username.strip()

            if not username or not password:

                st.error(
                    "Please enter username and password."
                )

            else:

                user = get_user(
                    username
                )

                if user and verify_password(
                    password,
                    user["password_hash"]
                ):

                    st.session_state.authenticated = True

                    st.session_state.username = username

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

    # =================================
    # REGISTER
    # =================================

    with register_tab:

        st.subheader(
            "Create Account"
        )

        new_username = st.text_input(
            "Choose a username",
            key="register_username"
        )

        new_password = st.text_input(
            "Choose a password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            key="confirm_password"
        )

        if st.button(
            "Create Account",
            type="primary",
            key="register_button"
        ):

            new_username = new_username.strip()

            # Username validation

            if not new_username:

                st.error(
                    "Username cannot be empty."
                )

            elif len(new_username) < 3:

                st.error(
                    "Username must be at least 3 characters."
                )

            # Password validation

            elif len(new_password) < 8:

                st.error(
                    "Password must be at least 8 characters."
                )

            # Confirm password

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                password_hash = hash_password(
                    new_password
                )

                created = create_user(
                    new_username,
                    password_hash
                )

                if created:

                    st.success(
                        "Account created successfully! "
                        "Go to the Login tab."
                    )

                else:

                    st.error(
                        "Username already exists."
                    )

    return False


# =================================
# CHECK AUTHENTICATION
# =================================

if "authenticated" not in st.session_state:

    st.session_state.authenticated = False


if not st.session_state.authenticated:

    authentication_page()

    st.stop()


# =================================
# MAIN APPLICATION
# =================================

st.title(
    "🤖 AI Software Development Team"
)

st.write(
    f"Welcome, **{st.session_state.username}** 👋"
)


# --------------------------------
# Logout
# --------------------------------

if st.button(
    "🚪 Logout"
):

    st.session_state.authenticated = False

    st.session_state.username = ""

    st.rerun()


st.divider()


# =================================
# PROJECT INPUT
# =================================

st.subheader(
    "🚀 Create a Software Project"
)


project_idea = st.text_area(
    "What do you want to build?",
    placeholder=(
        "Example: Build an online bookstore"
    ),
    height=120
)


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

                    fail_project(error)


            thread = threading.Thread(
                target=run_project,
                daemon=True
            )

            thread.start()

            st.success(
                "AI team started!"
            )


# =================================
# LIVE STATUS
# =================================

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


# =================================
# PROJECT HISTORY
# =================================

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