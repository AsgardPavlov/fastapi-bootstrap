from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import add_pagination
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware

from config import ENVIRONMENT
from database import sync_engine
from src.auth.admin import UserAdmin, admin_authentication_backend
from src.auth.router import auth_router

app_configs = {"title": "FastAPI Boostrap API"}

if ENVIRONMENT == "production":
    app_configs["openapi_url"] = None
    allow_origins = [
        # TODO PUT HERE YOUR PRODUCTION SITE URL
        "http://localhost:3000",
    ]
else:
    allow_origins = [
        "http://localhost:3000",
    ]

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Third party apps
add_pagination(app)
admin = Admin(
    app=app,
    engine=sync_engine,
    authentication_backend=admin_authentication_backend,
    title="PhysTech Admin",
)
templates = Jinja2Templates(directory="templates")

# Admin
admin.add_view(UserAdmin)

# Routers
app.include_router(auth_router)


@app.get("/privacy-policy", response_class=HTMLResponse)
def privacy_policy(request: Request):
    return templates.TemplateResponse(
        name="privacy-policy.html", context={"request": request}
    )


@app.get("/terms-and-conditions", response_class=HTMLResponse)
async def terms_and_conditions(request: Request):
    return templates.TemplateResponse(
        name="terms-and-conditions.html", context={"request": request}
    )
