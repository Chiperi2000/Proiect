from typing import type_check_only
import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
%matplotlib tk
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output=True,
    frames_per_buffer=CHUNK
)

data = stream.read(CHUNK)
data_int = struct.unpack(str(2*CHUNK)+ 'B',data)