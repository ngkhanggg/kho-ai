from fastapi import FastAPI
from app.auth_router import router as auth_router
app = FastAPI(title="KhoAI API")
app.include_router(auth_router)
@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
