"""
main.py - FastAPI Application Entry Point.
Run: uvicorn main:app --reload --port 8000
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from app.routers import health_router, content_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router.router)
app.include_router(content_router.router, prefix="/api/v1")


@app.get("/")
def root():
    return {
        "service": settings.PROJECT_NAME,
        "docs": f"http://localhost:8000{settings.DOCS_URL}",
        "generate_endpoint": "POST /api/v1/content/generate",
        "voices_endpoint": "GET /api/v1/content/voices",
        "platforms_endpoint": "GET /api/v1/content/platforms",
        "mode": "mock" if settings.is_mock_mode else "live_llm",
    }


if __name__ == "__main__":
    print(f"""
╔══════════════════════════════════════════════════════════╗
║   ✍️  AI CONTENT SYNDICATION ENGINE — Day 133             ║
║   Interactive Swagger Docs: http://localhost:8000/docs   ║
╚══════════════════════════════════════════════════════════╝
    """)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)