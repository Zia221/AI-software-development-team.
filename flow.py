from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel

from main import crew
from status import complete_project, fail_project
from logging_config import logger


class SoftwareDevelopmentState(BaseModel):

    project_idea: str = ""

    crew_result: str = ""


class SoftwareDevelopmentFlow(
    Flow[SoftwareDevelopmentState]
):

    @start()
    def start_project(self):

        logger.info(
            "Starting software project: %s",
            self.state.project_idea
        )

        print("🚀 Starting software project...")

        print(
            "Project:",
            self.state.project_idea
        )

        return self.state.project_idea


    @listen(start_project)
    def run_ai_team(
        self,
        project_idea
    ):

        logger.info(
            "Starting AI team for: %s",
            project_idea
        )

        print(
            "\n🤖 Starting AI Software Development Team..."
        )

        print(
            "Project:",
            project_idea
        )

        try:

            result = crew.kickoff(
                inputs={
                    "project_idea": project_idea
                }
            )

            self.state.crew_result = str(result)

            complete_project(result)

            logger.info(
                "Project completed successfully"
            )

            return self.state.crew_result

        except Exception as error:

            logger.exception(
                "AI team failed"
            )

            print(
                "❌ Project failed:",
                error
            )

            fail_project(error)

            self.state.crew_result = ""

            return "Project failed."