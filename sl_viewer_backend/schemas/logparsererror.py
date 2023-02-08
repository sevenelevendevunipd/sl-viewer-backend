from pydantic import BaseModel

class LogParserError(BaseModel):
    errors: list[str]