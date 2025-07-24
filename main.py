from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.database import Base, engine
from app.users.routers import router as user_router
from app.posts.routers import router as post_router
from app.auth.routers import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Mini Blog API",
        version="1.0",
        description="API with JWT authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # 👇 Add this to enforce BearerAuth globally (IMPORTANT!)
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

