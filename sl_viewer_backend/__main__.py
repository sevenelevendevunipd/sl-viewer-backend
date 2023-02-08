import uvicorn

uvicorn.run('sl_viewer_backend:app', log_level='info', reload=True)