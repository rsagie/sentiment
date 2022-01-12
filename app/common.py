from pydantic import Field, BaseModel
from typing import NamedTuple, List
from enum import Enum


class TextType(str, Enum):
    article = 'article'
    conversation = 'conversation'


class CustomModel(BaseModel):
    text: str = Field(...)
    type: TextType = Field(..., description='Input text type')
    url: str = Field(..., description='URL link for the remote skill')
    auth_key: str = Field(..., description='Auth key of the remote url')
