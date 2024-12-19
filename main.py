from fastapi import FastAPI, APIRouter

from Controller import artists_controller

app = FastAPI()

router = APIRouter()

router.include_router(artists_controller.router, tags=["artists"])
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}