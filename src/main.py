import uvicorn
from fastapi import FastAPI

from .app.config import settings
from .auth.auth import router as auth_router
from .app.routes import router as api_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.run.host, port=settings.run.port, reload=False)
