#!/usr/bin/env sh

. ./.venv/bin/activate
./.venv/bin/gunicorn -k uvicorn.workers.UvicornWorker -w $((2 * $(nproc))) -b 0.0.0.0:8000 --access-logfile - sl_viewer_backend:app