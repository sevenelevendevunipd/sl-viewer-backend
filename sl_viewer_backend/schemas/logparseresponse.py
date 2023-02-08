from pydantic import BaseModel

from sl_parser import LogFile

class LogParserResponse(BaseModel):
    log: LogFile