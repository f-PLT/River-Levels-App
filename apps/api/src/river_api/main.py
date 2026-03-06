from fastapi import FastAPI

app = FastAPI(title="River Levels API")


@app.get("/")
async def root():
    return {"message": "Hello from River Levels API"}
