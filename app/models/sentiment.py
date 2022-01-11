import logging
from typing import List
from textblob import TextBlob

from app.api.pipeline.output_model import PipelineOutput, OutputBlock
from app.common import Status

logger = logging.getLogger(__name__)

async def get_sentiment(input_text):
    logger.info(f'Handling request')

    #input_text = "Sure it looks line it has some intersting feature"
    analysis = TextBlob(input_text)
    print(analysis.sentiment.polarity)
    sentiment = ""
    if analysis.sentiment.polarity > 0:
        sentiment = "positive"
    else:
        sentiment = "negative"

    output_block: OutputBlock = OutputBlock(
        text_generated_by_step_name='Generating step name',
        text_generated_by_step_id=0,
        text='Output text',
        labels=[])

    output_blocks: List[OutputBlock] = [output_block]
    output: PipelineOutput = PipelineOutput(input_text=input_text, status=Status.success,
                                            output=output_blocks)
    output.input_text = input_text

    return output
