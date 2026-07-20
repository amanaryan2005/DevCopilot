from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import AgentState
from app.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=settings.GOOGLE_API_KEY
)

def synthesize_report(state: AgentState) -> dict:
    prompt = f"""Synthesize the following security analysis and organizational policies into a clean GitHub PR review comment.

### Security Findings:
{state.get('security_issues', 'None')}

### Organizational Compliance Rules:
{state.get('policy_context', 'None')}

Generate a clear, actionable summary with recommended fixes."""

    messages = [
        SystemMessage(content="You generate automated code review summaries for developers."),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)
    return {"final_report": response.content}