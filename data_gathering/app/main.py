from fastapi import FastAPI
from app.api.routers import router_files
from app.api.database.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/data_gathering/openapi.json",
              docs_url="/api/v1/data_gathering/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

for router_file in router_files:
    app.include_router(router_file.router, prefix='/api/v1/data_gathering',
                       tags=['data_gathering'])
