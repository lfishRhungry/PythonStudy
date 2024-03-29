import wave
import math
import numpy as np

sRate = 44100
nSamples = sRate * 5
x = np.arange(nSamples) / float(sRate)
vals = np.sin(2.0 * math.pi * 220.0 * x)
data = np.array(vals * 32767, "int16").tostring()
file = wave.open("sine200.wav", "wb")
file.setparams(1, 2, sRate, nSamples, "NONE", "uncompressed")
file.writeframes(data)
file.close()