from crewai.tools import tool
import chromadb


# ==================================================
# PROJECT INFORMATION TOOL
# ==================================================

@tool("project_info")
def project_info() -> str:
    """Returns information about the AI software development project."""

    return """
    Project Name:
    AI Software Development Team

    Purpose:
    Build software using a team of specialized AI agents.

    Team:
    - Product Manager
    - Software Architect
    - Software Developer
    - QA Engineer

    Workflow:
    Requirements -> Architecture -> Development -> Testing
    """


# ==================================================
# CHROMADB
# ==================================================

client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="project_knowledge"
)


# ==================================================
# RAG SEARCH TOOL
# ==================================================

@tool("search_project_knowledge")
def search_project_knowledge(query: str) -> str:
    """Search the project knowledge base for relevant information."""

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    documents = results.get("documents", [])

    if not documents or not documents[0]:
        return "No relevant knowledge found."

    return "\n\n".join(documents[0])


# ==================================================
# TEST RAG TOOL
# ==================================================

if __name__ == "__main__":

    result = search_project_knowledge.run(
        "How should API keys be handled?"
    )

    print(result)