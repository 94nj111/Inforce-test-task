from fastapi import FastAPI

from routers.accounts import router as accounts_router
from routers.restaurants import router as restaurants_router

app = FastAPI(title="restaurant", version="0.1.0", description="Inforce Test Task")
app.include_router(accounts_router)
app.include_router(restaurants_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
