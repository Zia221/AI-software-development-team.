from fastapi import (
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    HTTPException
)

from fastapi.responses import FileResponse

from pydantic import BaseModel

from threading import Thread

import asyncio

from flow import SoftwareDevelopmentFlow

from status import (
    start_project,
    get_status
)

from logging_config import logger


app = FastAPI(
    title="AI Software Development Team",
    version="1.0.0"
)


class ProjectRequest(BaseModel):

    project_idea: str


@app.get("/")
def home():

    return FileResponse(
        "index.html"
    )


@app.post("/projects")
def create_project(
    request: ProjectRequest
):

    project_idea = request.project_idea.strip()

    if not project_idea:

        raise HTTPException(
            status_code=400,
            detail="Project idea cannot be empty."
        )

    try:

        start_project(
            project_idea
        )

        def run_flow():

            try:

                flow = SoftwareDevelopmentFlow()

                flow.state.project_idea = project_idea

                flow.kickoff()

            except Exception:

                logger.exception(
                    "Background Flow failed"
                )


        Thread(
            target=run_flow,
            daemon=True
        ).start()


        return {
            "message": "Project started!",
            "project_idea": project_idea
        }

    except Exception as error:

        logger.exception(
            "Could not start project"
        )

        raise HTTPException(
            status_code=500,
            detail="Could not start project."
        ) from error


@app.get("/status")
def status():

    return get_status()


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    try:

        while True:

            current_status = get_status()

            await websocket.send_json(
                current_status
            )

            if current_status["project"]["state"] in [
                "completed",
                "error"
            ]:

                break

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:

        logger.info(
            "WebSocket disconnected"
        )