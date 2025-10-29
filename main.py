from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import engine
from app.models import Base
from app.routers import users
from app.error_handlers import user_already_exists_exception_handler,user_not_found_exception_handler
from app.exceptions import UserAlreadyExistsError,UserNotFoundError

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield  
    print("🛑 Shutting down app...")

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "FastAPI User Microservice Running!"}

# Register custom error handlers
app.add_exception_handler(UserNotFoundError, user_not_found_exception_handler)
app.add_exception_handler(UserAlreadyExistsError, user_already_exists_exception_handler)
