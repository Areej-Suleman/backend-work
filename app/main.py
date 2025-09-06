from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.core.db import engine
from app.models import Base
from app.services.notifications_service import send_morning_reminder, send_evening_reminder

# ✅ Import routers individually
from app.api.v1 import (
    products,
    users,
    upload,
    chat,
    auth,
    brands,
    profile,
    recommend,
    recommendations,
    reminders,
    analysis,
    admin
)

app = FastAPI(
    title="GlowGenius API",
    description="Backend for GlowGenius platform",
    version="1.0.0"
)

scheduler = BackgroundScheduler()

@app.on_event("startup")
async def startup_event():
    # Base.metadata.create_all(bind=engine) # Uncomment if you want to create tables on startup
    
    # Schedule daily reminders
    scheduler.add_job(send_morning_reminder, 'cron', hour=8, minute=0, id='morning_reminder')
    scheduler.add_job(send_evening_reminder, 'cron', hour=20, minute=0, id='evening_reminder')
    
    scheduler.start()
    print("Scheduler started and jobs added.")

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()
    print("Scheduler shut down.")

# ✅ Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root endpoint for health check
@app.get("/")
def read_root():
    return {"message": "GlowGenius API is running 🚀"}

# ✅ Register routers
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(upload.router, prefix="/api/v1/upload", tags=["Upload"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(brands.router, prefix="/api/v1/brands", tags=["Brands"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(recommend.router, prefix="/api/v1/recommend", tags=["Recommend"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(reminders.router, prefix="/api/v1/reminders", tags=["Reminders"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
