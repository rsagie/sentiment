from typing import Optional

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi import Request, Header

from app.api.pipeline.output_model import PipelineOutput
from app.models.sentiment import get_sentiment

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/sentiment", response_model=PipelineOutput, response_description="Processed request",
          response_model_exclude_unset=True)
#async def sentiment_api(request: Request, access_token: Optional[str] = Header(None)):
async def sentiment_api(request: Request):
    res = await get_sentiment(request,input_text="")
    if res:
        return res
    return None


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9080, reload=True)
