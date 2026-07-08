from claude_agent_sdk import AgentDefinition

from app.agents.search_agent import build_search_agent
from app.agents.document_agent import build_document_agent
from app.agents.synthesis_agent import build_synthesis_agent
from app.agents.report_agent import build_report_agent


def build_agents() -> dict[str, AgentDefinition]:
    return {
        "search-agent": build_search_agent(),
        "document-agent": build_document_agent(),
        "synthesis-agent": build_synthesis_agent(),
        "report-agent": build_report_agent(),
    }
