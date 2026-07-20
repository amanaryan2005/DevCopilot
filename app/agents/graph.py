from langgraph.graph import StateGraph, START, END
from app.agents.state import AgentState
from app.agents.security import run_security_scan
from app.agents.rag import fetch_policy_context
from app.agents.supervisor import synthesize_report

# 1. Initialize Graph
builder = StateGraph(AgentState)

# 2. Add Nodes
builder.add_node("security_node", run_security_scan)
builder.add_node("rag_node", fetch_policy_context)
builder.add_node("supervisor_node", synthesize_report)

# 3. Add Edges (Parallel Execution -> Supervisor)
builder.add_edge(START, "security_node")
builder.add_edge(START, "rag_node")
builder.add_edge("security_node", "supervisor_node")
builder.add_edge("rag_node", "supervisor_node")
builder.add_edge("supervisor_node", END)

# 4. Compile Graph
copilot_graph = builder.compile()