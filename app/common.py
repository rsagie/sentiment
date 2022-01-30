
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
    type: str = Field(..., description='Label type')
    name: Optional[str] = Field(None, description='Label name')
    span: Union[Span, None] = Field(..., description='Origin span')
    value: Union[str, float, None] = Field(..., description='Value')
    origin: Optional[str] = Field(None, description='Origin value')
    output_spans: List[OutputSpan] = Field(..., description='Utterance spans')
    input_spans: List[OutputSpan] = Field(None, description='Origin utterance spans')
    span_text: Union[str, None] = Field(..., description='Span text')


class CustomModel(BaseModel):
    text: str = Field(...)
    type: TextType = Field(..., description='Input text type')
    url: str = Field(None, description='URL link for the remote skill')
    labels: List[Label] = Field([], description='Labels')
    params: Dict = Field({}, description='Custom skill parameters')
