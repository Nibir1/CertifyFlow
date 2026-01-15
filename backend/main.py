"""
Main Application Entry Point
----------------------------
This file initializes the FastAPI application, configures CORS to allow
frontend communication, and defines the basic health check endpoint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Initialize FastAPI app with project metadata
app = FastAPI(
    title="CertifyFlow API",
    description="AI-Assisted FAT/SAT Procedure Generation Engine",
    version="0.1.0"
)

# CORS Configuration
# We explicitly allow the frontend origin to prevent CORS errors during development
origins = [
    "http://localhost:5173",  # Vite Frontend default port
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health", tags=["System"])
async def health_check():
    """
    System Health Check
    -------------------
    Simple endpoint to verify backend is running and reachable.
    Returns: JSON response with status 'ok'.
    """
    return JSONResponse(content={"status": "ok", "service": "CertifyFlow Backend"})

if __name__ == "__main__":
    import uvicorn
    # Run the server directly for debugging purposes
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)