from fastapi import FastAPI
from routes.user import user
from routes.portal import portal
app = FastAPI()

app.include_router(user)
app.include_router(portal)


