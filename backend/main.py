from fastapi import FastAPI

#initializing Mindora

app = FastAPI(
    title="Mindora API",
    description="Backend for TRIBE V2 neural response prediction",
    version="1.0.0",
)
@app.get("/")
async def root():
    return {"message": "Welcome to the Mindora API!"}
@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": False}