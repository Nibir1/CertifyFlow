"""
Main Application Entry Point
----------------------------
This file initializes the FastAPI application, configures CORS to allow
frontend communication, and defines the basic health check endpoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import the new router
from app.api.routes import router as gen_router

app = FastAPI(
    title="CertifyFlow API",
    description="AI-Assisted FAT/SAT Procedure Generation Engine",
    version="0.1.0"
)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the Generation Router
app.include_router(gen_router, prefix="/api/v1", tags=["Generation"])

@app.get("/health", tags=["System"])
async def health_check():
    return JSONResponse(content={"status": "ok", "service": "CertifyFlow Backend"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)