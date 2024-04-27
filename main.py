from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routes.home import homeRoutes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(homeRoutes, prefix="/home", tags=["home"])
