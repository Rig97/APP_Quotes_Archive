# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import quotes, users


# Create all database tables (runs on startup if tables don't exist)
models.Base.metadata.create_all(bind=engine)


app = FastAPI(title='Quotes Archive API', version='1.0.0')


# CORS: allow the frontend to call the backend
# (Without this, browsers block requests between different origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # In production, change this to your exact domain
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


# Register the routers
app.include_router(users.router)
app.include_router(quotes.router)


@app.get('/')
def root():
    return {'message': 'Quotes Archive API is running'}
