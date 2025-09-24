from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from app.api.routes.routers import router_files
from app.api.database.db import metadata, database, DATABASE_URI
from app.auth.api_key import verify_api_key
from sqlalchemy import create_engine

def metadata_dump(sql, *multiparams, **params):
    # print or write to log or file etc
    print(sql.compile(dialect=engine.dialect))

#engine = create_engine(DATABASE_URI, strategy='mock', executor=metadata_dump)
engine = create_engine(DATABASE_URI, echo=True)
metadata.create_all(engine,checkfirst=True)

title = "Fleet control API"
openapi_url = "/api/violette/v2/openapi.json"
favicon_url = "https://natuition.com/wp-content/uploads/2019/11/1-1-150x150.png"
version="2.0.0"
description = """
It's an API to which allows Violette robot to upload their data. 
Also allows you to recover all the data sent from robots in order to use them in different software
"""

app = FastAPI(openapi_url=openapi_url,
              docs_url=None,
              redoc_url=None,
              title=title,
              description=description,
              version=version,
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
	return get_swagger_ui_html(openapi_url=openapi_url, title=title, swagger_favicon_url=favicon_url, swagger_ui_parameters={"docExpansion": "none"})

@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
	return get_redoc_html(openapi_url=openapi_url, title=title, redoc_favicon_url=favicon_url)