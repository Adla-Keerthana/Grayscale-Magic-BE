from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_routes, protected_routes

app = FastAPI()

# Add CORS middleware for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://grayscale-magic-fe.vercel.app"],  # Local frontend URL (adjust port as needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(protected_routes.router, prefix="/protected", tags=["protected"])

@app.get("/login")
async def root():
    return {"message": "Hello, World!"}
