from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import AgentState
from app.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=settings.GOOGLE_API_KEY
)

def run_security_scan(state: AgentState) -> dict:
    prompt = f"""Perform an OWASP Top 10 security audit on this code diff:

Repository: {state['repository']}
Diff:
{state['code_diff']}

Highlight any exposed secrets, SQL injection, insecure dependencies, or unhandled exceptions."""

    messages = [
        SystemMessage(content="You are a Principal Security Auditor specializing in DevSecOps."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return {"security_issues": response.content}