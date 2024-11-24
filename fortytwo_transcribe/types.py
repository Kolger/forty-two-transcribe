from pydantic import BaseModel

class AIResponse(BaseModel):
    content: str
    provider: str
    error: bool = False
