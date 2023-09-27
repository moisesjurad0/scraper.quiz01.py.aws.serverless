from api.api_v1.api import router as api_router
from fastapi import FastAPI, Request  # , stage
from mangum import Mangum
# from mangum import Mangum, Contex
import os
import logging
from fastapi.middleware.cors import CORSMiddleware


APP_NAME = os.getenv('APP_NAME', default='m01')
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO)
logger.info(f'm01.APP_NAME=>{APP_NAME}')


# stage = mangum.context.get_stage()
# root_path = os.environ['SERVERLESS_STAGE']
root_path = os.getenv('SERVERLESS_STAGE', default='')
logger.info(f'm01.SERVERLESS_STAGE=>{root_path}')
root_path = os.getenv('MY_STAGE', default='')
logger.info(f'm01.MY_STAGE=>{root_path}')

description = """
QuestionsAPI helps you do operations with the scraped data. 🚀

## Questions

You will be able to:

* **Put questions** (Create & Update & batch).
* **Read questions**.
* **Search questions**.
"""

app = FastAPI(
    title="QuestionsAPI",
    description=description,
    summary="do a CRUD of Questions/Answers.",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "moisesjurad0",
        "url": "https://linktr.ee/moisesjurad0",
        # "email": "moises003@outlook.com",
    },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
    root_path=f'/{root_path}'
)


# app = FastAPI(root_path=f'/{root_path}')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# async def root():
#     return {"message`": "Hello World!"}


# @app.get("/url")
# async def url(request: Request):
#     url = request.url
#     print(f"url: {url}")
#     logging.info(f"La URL completa es: {url}")
#     return url


@app.get("/ok")
@app.get("/test")
async def test_ok():
    ok = 'ok'
    print(ok)
    logging.info(ok)
    return ok

app.include_router(api_router, prefix="/api/v1")

handler = Mangum(app)
