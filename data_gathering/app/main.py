from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.routers import router_files
from app.api.database.db import metadata, database, DATABASE_URI
from sqlalchemy import create_engine
import logging

engine = create_engine(DATABASE_URI)
metadata.create_all(engine)
logger = logging.getLogger("uvicorn")

description = """
It's an API to which allows Violette robot to upload their data.

You can acces to robots web socket of here : [/api/v1/data_gathering/ws_robot_view](/api/v1/data_gathering/ws_robot_view).
"""

app = FastAPI(openapi_url="/api/v1/data_gathering/openapi.json",
              docs_url="/api/v1/data_gathering/docs",
              swagger_ui_parameters={"docExpansion": "none"},
              title="Data gathering",
              description=description,
              version="1.0.0",
              contact={"name": "Vincent LAMBERT",
                       "email": "v.lambert@natuition.com"}
              )

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    for router_file, tag_name in router_files:
        app.include_router(router_file.router, prefix='/api/v1/data_gathering',
                           tags=[tag_name])
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
