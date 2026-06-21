from pydantic import BaseModel, Field
from typing import List, Optional

class GitHubIssue(BaseModel):
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str

class WebhookPayload(BaseModel):
    action: str
    issue: GitHubIssue

class ParsedASTNode(BaseModel):
    name: str
    type: str
    code_snippet: str
    start_line: int
    end_line: int

class TestResult(BaseModel):
    passed: bool
    output: str
    error_message: Optional[str] = None
