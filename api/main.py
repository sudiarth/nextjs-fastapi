from fastapi import (
    FastAPI,
)
from api.routes import indodax

app = FastAPI()

app.include_router(
    indodax.router,
    prefix="/api",
    responses={418: {"description": "I'm a teapot"}},
)

