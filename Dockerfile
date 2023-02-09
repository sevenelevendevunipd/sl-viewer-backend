# Build venv in a separate stage in order to minimize final image size
FROM python:3.10-alpine AS builder
ARG WORKDIR

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
RUN apk add openssh gcc musl-dev libffi-dev && pip install poetry && poetry config virtualenvs.in-project true && mkdir /root/.ssh && ssh-keyscan github.com >> /root/.ssh/known_hosts
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN --mount=type=ssh,id=github_ssh_key poetry install -n --no-root



FROM python:3.10-alpine

ARG WORKDIR
WORKDIR /app
COPY --from=builder /app .
COPY entrypoint.sh .
COPY sl_viewer_backend sl_viewer_backend

ENTRYPOINT [ "/app/entrypoint.sh" ]
