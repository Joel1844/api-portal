from fastapi import FastAPI
from routes.user import user
from routes.portal import portal
from dotenv import load_dotenv
from os import getenv
load_dotenv()

from auth.route import router as auth_routes
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes)
app.include_router(user)
app.include_router(portal)

# app.mount("/", StaticFiles(directory=os.path.abspath(
#     "./app/build").replace("\\", "/"), html=True), name="app")


