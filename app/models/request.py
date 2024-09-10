from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class AnswerRequest(BaseModel):
    context: str
