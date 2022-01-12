from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field


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

    @staticmethod
    def create_label(type, start, end, value, text, segment_start, section_index, name=None, input_section_index=None,
                     input_start=0, input_end=0):
        return Label(type=type, value=value,
                     span=[start + segment_start, end + segment_start],
                     output_spans=[{"section": section_index, "start": start, "end": end}],
                     input_spans=[{"section": input_section_index, "start": input_start, "end": input_end}] if input_section_index else None,
                     span_text=text[start:end], name=name)

    @staticmethod
    def create_label_no_spans(type, value, name=None):
        return Label(type=type, value=value, name=name, span=None, span_text=None, output_spans=[])

class SkillOutput(BaseModel):
    labels: List[Label] = Field([], description='Labels')

