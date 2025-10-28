from contextlib import asynccontextmanager

from fastapi import FastAPI

from apprise_api_headless.config import Settings
from apprise_api_headless.metrics import setup_metrics
from apprise_api_headless.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.state.settings = settings
    yield


app = FastAPI(title="Apprise API", lifespan=lifespan)
app.include_router(router=router)
setup_metrics(app)
