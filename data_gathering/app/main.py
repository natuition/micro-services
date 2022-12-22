from fastapi import FastAPI
from app.api.routes.routers import router_files
from app.api.database.db import metadata, database, DATABASE_URI
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URI)
metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/data_gathering/openapi.json",
              docs_url="/api/v1/data_gathering/docs")


@app.on_event("startup")
async def startup():
    for router_file, tag_name in router_files:
        app.include_router(router_file.router, prefix='/api/v1/data_gathering',
                           tags=[tag_name])
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
