from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    code_diff: str
    repository: str
    security_issues: Optional[str]
    policy_context: Optional[str]
    final_report: Optional[str]