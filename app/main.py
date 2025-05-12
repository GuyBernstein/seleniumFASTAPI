from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.controllers.app_controller import router as app_router
from app.controllers.selenium_controller import router as selenium_router

app = FastAPI(title="Grocery List Hub")

# Include routers
app.include_router(app_router)
app.include_router(selenium_router, prefix="/api/selenium", tags=["selenium"])


# Custom OpenAPI schema (similar to Swagger config in Spring)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Grocery List API",
        version="1.0.0",
        description="FastAPI version of Grocery List application",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)