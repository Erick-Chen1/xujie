from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
