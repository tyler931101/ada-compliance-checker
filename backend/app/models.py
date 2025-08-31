from pydantic import BaseModel
from typing import List, Optional

class AccessibilityViolation(BaseModel):
    ruleId: str
    message: str
    element: str
    selector: str
    codeSnippet: str

class HtmlRequest(BaseModel):
    html: str

class CheckResponse(BaseModel):
    violations: List[AccessibilityViolation]