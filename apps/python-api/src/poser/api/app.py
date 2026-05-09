from __future__ import annotations

from fastapi import FastAPI

from poser.api.routes_render import router

app = FastAPI(title="Poser API", version="0.1.0")
app.include_router(router, prefix="/v1")
