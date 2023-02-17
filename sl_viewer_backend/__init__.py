from spectree import SpecTree
from spectree import Response as SpectreeResponse
from starlette.applications import Starlette
from starlette.datastructures import UploadFile
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, Mount

from sl_parser import LogFile

from .schemas import LogUpload, LogParserResponse, LogParserError

spec = SpecTree("starlette")

@spec.validate(form=LogUpload, resp=SpectreeResponse(HTTP_200=LogParserResponse, HTTP_422=LogParserError))
async def analyze_log(request) -> Response:
    form: LogUpload = request.context.form
    log_file = form.log
    if not isinstance(log_file, UploadFile) or log_file.content_type != "text/csv":
        return JSONResponse(dict(LogParserError(errors=["Invalid log file"])), status_code=422)
    content = await log_file.read()
    try:
        return Response(LogParserResponse(log=LogFile.parse_log(log_file.filename, content.decode('cp1252'))).json(), media_type="application/json")
    except Exception as e:
        return JSONResponse(LogParserError(errors=[f"Log parsing error: {repr(e)[:64]}"]).dict(), status_code=422)


app = Starlette(debug=True, routes=[
    Mount('/api', routes=[
        Route('/analyze_log', analyze_log, methods=['POST']),
    ]),
], middleware=[
    Middleware(CORSMiddleware, allow_origins=['*'])
])

spec.register(app)
