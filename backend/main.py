from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import images, masks, recolor, history

app = FastAPI(
    title="Car Color Studio API",
    description="API for the Car Color Studio application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(images.router, prefix="/api", tags=["images"])
app.include_router(masks.router, prefix="/api", tags=["masks"])
app.include_router(recolor.router, prefix="/api", tags=["recolor"])
app.include_router(history.router, prefix="/api", tags=["history"])

@app.get("/")
async def root():
    return {"message": "Welcome to Car Color Studio API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0", port=8000, reload=True)
