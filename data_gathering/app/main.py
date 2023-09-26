from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from app.api.routes.routers import router_files
from app.api.database.db import metadata, database, DATABASE_URI
from app.auth.api_key import verify_api_key
from sqlalchemy import create_engine

engine = create_engine(DATABASE_URI)
metadata.create_all(engine)

description = """
It's an API to which allows Violette robot to upload their data. 
Also allows you to recover all the data sent from robots in order to use them in different software

You can acces to robots web socket of here : [/api/violette/v2/ws_robot_view](/api/violette/v2/ws_robot_view).
"""

app = FastAPI(openapi_url="/api/violette/v2/openapi.json",
              docs_url=None,
              redoc_url=None,
              title="Fleet control API",
              description=description,
              version="2.0.0",
              contact={"name": "Vincent LAMBERT",
                       "email": "v.lambert@natuition.com"}
              )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    for router_file, tag_name in router_files:
        app.include_router(router_file.router, prefix='/api/violette/v2',
                           tags=[tag_name], dependencies=[Depends(verify_api_key)])
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get('/favicon.png', include_in_schema=False)
async def favicon():
    return FileResponse("./icon.png")

@app.get("/docs", include_in_schema=False)
def overridden_swagger():
	return get_swagger_ui_html(openapi_url="/api/violette/v2/openapi.json", title="FastAPI", swagger_favicon_url="https://natuition.com/wp-content/uploads/2019/11/1-1-150x150.png", swagger_ui_parameters={"docExpansion": "none"})

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(openapi_url="/api/violette/v2/openapi.json", title="FastAPI", redoc_favicon_url="https://natuition.com/wp-content/uploads/2019/11/1-1-150x150.png")