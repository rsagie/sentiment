
from enum import Enum
from typing import List, Optional, Union, Dict
from pydantic import BaseModel, Field


class TextType(str, Enum):
    article = 'article'
    conversation = 'conversation'

class Span(BaseModel):
    __root__: List[int] = Field(..., max_items=2, min_items=2)

class OutputSpan(BaseModel):
    section: int = Field(..., description='Utterance index')
    start: int = Field(..., description='Start position')
    end: int = Field(..., description='End position')


class Label(BaseModel):
    span_text: Union[str, None] = Field(..., description='Span text')


class CustomModel(BaseModel):
    labels: List[Label] = Field([], description='Labels')
