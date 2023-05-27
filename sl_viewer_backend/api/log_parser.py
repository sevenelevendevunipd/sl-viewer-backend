from spectree import Response as SpectreeResponse
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from sl_viewer_backend import spec
from sl_viewer_backend.schemas import LogParserError, LogParserResponse, LogUpload
from sl_viewer_backend.services import log_parsing_service


@spec.validate(
    form=LogUpload,
    resp=SpectreeResponse(HTTP_200=LogParserResponse, HTTP_400=LogParserError),
    tags=["Log parsing"],
)
async def parse_log(request: Request) -> Response:
    form_data = await request.form()

    try:
        return Response(
            LogParserResponse(log=await log_parsing_service.parse_log_file(form_data)).json(),
            media_type="application/json",
        )
    except log_parsing_service.LogParsingServiceError as e:
        return JSONResponse(
            LogParserError(errors=[e.message]).dict(),
            status_code=400,
        )

LogParserRoute = Route("/parse_log", parse_log, methods=["POST"])
