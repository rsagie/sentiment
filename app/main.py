from typing import Optional

import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi import Request, Header

from app.api.pipeline.input_model import InputText
from app.api.pipeline.output_model import SkillOutput
from app.models.sentiment import get_sentiment

app = FastAPI()


@app.post("/sentiment", response_model=SkillOutput, response_description="Processed request",
          response_model_exclude_unset=True)
async def sentiment_api(req_body: InputText, request: Request):
    res = await get_sentiment(input_text=req_body.input_text)
    if res:
        return res
    return None


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9080, reload=True)
