from sl_parser import LogFile
from starlette.datastructures import FormData, UploadFile

from ..schemas import LogUpload
from ..validation import ValidationError
from ..validation.log_upload import validate_log_file


class LogParsingServiceError(Exception):
    message: str

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(*args)
        self.message = message


async def parse_log_file(form_data: FormData) -> LogFile:
    form = LogUpload(**form_data)  # type: ignore
    log_file: UploadFile = form.log  # type: ignore
    try:
        validate_log_file(log_file)
    except ValidationError as e:
        raise LogParsingServiceError("Invalid log file") from e

    content = await log_file.read()
    try:
        return LogFile.parse_log(log_file.filename or "<empty>", content.decode("cp1252"))
    except Exception as e:
        raise LogParsingServiceError(f"Log parsing error: {repr(e)[:64]}") from e
