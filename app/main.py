from typing import Optional

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi import Request, Header

from app.common import CustomModel
from app.api.pipeline.output_model import SkillOutput
from app.models.cluster import cluster_texts_api
from app.models.sentiment import get_sentiment

app = FastAPI()


@app.post("/sentiment", response_model=SkillOutput, response_description="Processed request",
          response_model_exclude_unset=True)
async def sentiment_api(req_body: CustomModel, request: Request):
    res = await get_sentiment(input_text=req_body.text)
    if res:
        return res
    return None


@app.post("/cluster", response_model=SkillOutput, response_description="Processed request",
          response_model_exclude_unset=True)
async def cluster_api(req_body: CustomModel, request: Request):
    res = await cluster_texts_api(req_body)
    if res:
        return res
    return None

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9080, reload=True)
