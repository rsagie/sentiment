from pydantic import Field, BaseModel
from typing import NamedTuple, List
from enum import Enum


class Status(str, Enum):
    success = 'success'
    failure = 'failure'


class TextType(str, Enum):
    article = 'article'
    conversation = 'conversation'

class TextSegment(NamedTuple):
    start: int = Field(...)
    end: int = Field(...)
    text: str = Field(...)
    meta: str = Field('')


class TextSegmentList(BaseModel):
    segments: List[TextSegment] = Field(default=[])
    type: TextType = Field(...)
