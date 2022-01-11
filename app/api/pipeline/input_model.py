from enum import Enum

from pydantic import BaseModel, Field

from app.common import TextType, TextSegment


class InputText(BaseModel):
    input_text: str = Field("Sure it looks line it has some interesting features", description='Input text')


