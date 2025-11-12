from fastapi import FastAPI

from app.routers import register_routers

app = FastAPI(title="Хайталент",
              version="1.0.0")
register_routers(app)


@app.get("/")
async def welcome():
    return {"message": "Welcome to Хайталент"}
