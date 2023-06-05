from starlette.datastructures import UploadFile

from . import ValidationError


def validate_log_file(log_file: UploadFile) -> None:
    if not isinstance(log_file, UploadFile) or log_file.content_type not in {"text/csv", "application/vnd.ms-excel"}:
        raise ValidationError()
