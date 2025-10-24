from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from apprise_api_headless.config import Settings
from apprise_api_headless.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.state.settings = settings
    yield


app = FastAPI(title="Apprise API", lifespan=lifespan)
app.include_router(router=router)
Instrumentator().instrument(app).expose(app)
