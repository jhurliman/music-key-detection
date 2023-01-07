import json
import numpy as np

from base64 import b64decode
from datetime import datetime
from os import remove
from essentia import Pool
from essentia.standard import (
    FrameGenerator,
    HPCP,
    Key,
    MonoLoader,
    SpectralPeaks,
    Spectrum,
    Windowing,
)

FRAME_SIZE = 2048
HOP_SIZE = 1024


def detect_key(audio):
    spec = Spectrum(size=FRAME_SIZE)
    spec_peaks = SpectralPeaks()
    hpcp = HPCP()
    key = Key(profileType="edma")
    w = Windowing(type="blackmanharris92")
    pool = Pool()

    for frame in FrameGenerator(audio, frameSize=FRAME_SIZE, hopSize=HOP_SIZE):
        frame_spectrum = spec(w(frame))
        frequencies, magnitudes = spec_peaks(frame_spectrum)
        hpcpValue = hpcp(frequencies, magnitudes)
        pool.add("hpcp", hpcpValue)

    hpcp_avg = np.average(pool["hpcp"], axis=0)
    detected_key, scale, _, _ = key(hpcp_avg)
    return detected_key, scale


def handler(event, context):
    # Sanity check "filename" and "content" appear in the event
    if event is None or "filename" not in event or "content" not in event:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing filename or content"}),
            "headers": {"Content-Type": "application/json"},
        }

    # Get the filename and file extension from the event
    filename = event["filename"]
    extension = filename.split(".")[-1]

    # Base64 decode the file
    file_content = b64decode(event["content"])

    # Write the file to a temporary location
    tmp_filename = "input." + extension
    with open(tmp_filename, "wb") as f:
        f.write(file_content)

    # Load the audio file, resampled to a 44.1kHz mono signal
    loader = MonoLoader(filename=tmp_filename, sampleRate=44100)
    audio = loader()

    # Detect the key and scale
    key, scale = detect_key(audio)

    data = {
        "key": key,
        "scale": scale,
        "filename": filename,
        "filesize": len(file_content),
        "timestamp": datetime.utcnow().isoformat(),
    }

    # delete the temporary file
    remove(tmp_filename)

    return {
        "statusCode": 200,
        "body": json.dumps(data),
        "headers": {"Content-Type": "application/json"},
    }
