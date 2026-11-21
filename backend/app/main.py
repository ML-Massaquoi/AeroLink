from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, health, locations, racks, users
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Airport Network Infrastructure Management System",
        docs_url="/docs" if not settings.is_test else None,
        openapi_url="/openapi.json" if not settings.is_test else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_router_prefix = "/api/v1"
    app.include_router(health.router, prefix=api_router_prefix)
    app.include_router(auth.router, prefix=api_router_prefix)
    app.include_router(users.router, prefix=api_router_prefix)
    app.include_router(locations.router, prefix=api_router_prefix)
    app.include_router(racks.router, prefix=api_router_prefix)

    return app


app = create_app()
