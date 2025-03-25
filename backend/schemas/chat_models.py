from pydantic import BaseModel
from typing import Dict, List, Optional

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    intent: str
    confidence: float
    category: str
    entities: Optional[List[Dict[str, str]]] = {}