import logging
from typing import List
from textblob import TextBlob

from app.api.pipeline.output_model import Label, SkillOutput

logger = logging.getLogger(__name__)


async def get_sentiment(input_text):
    logger.info(f'Handling request')

    # input_text = "Sure it looks line it has some intersting feature"
    analysis = TextBlob(input_text)
    print(analysis.sentiment.polarity)
    if analysis.sentiment.polarity > 0:
        sentiment = "positive"
    else:
        sentiment = "negative"

    label = Label(type="custom", name="sentiment", span=None, value=sentiment,
                                 output_spans=[],
                                 input_spans=None, span_text=None)

    skill_output: SkillOutput = SkillOutput(labels=[label])

    return skill_output
