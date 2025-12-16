from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import Base, engine
from app.routes import auth, subscriptions, api_keys

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AgentsHome API", version="1.0.0")
settings = get_settings()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)
app.include_router(subscriptions.router)
app.include_router(api_keys.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "AgentsHome API", "version": "1.0.0"}
