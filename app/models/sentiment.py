import logging
from typing import List

from app.api.pipeline.output_model import PipelineOutput, OutputBlock
from app.common import Status

logger = logging.getLogger(__name__)


async def get_sentiment(request, input_text):
    logger.info(f'Handling request')

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
