from starlette.routing import Mount

from .log_parser import LogParserRoute

ApiMount = Mount("/api", routes=[
    LogParserRoute
])
