import json
import datetime

from essentia import Pool
from essentia.standard import (
    FrameGenerator,
    HPCP,
    Key,
    SpectralPeaks,
    Spectrum,
    Windowing,
)


def handler(event, context):
    data = {
        "output": "Hello World",
        "timestamp": datetime.datetime.utcnow().isoformat(),
    }
    return {
        "statusCode": 200,
        "body": json.dumps(data),
        "headers": {"Content-Type": "application/json"},
    }
