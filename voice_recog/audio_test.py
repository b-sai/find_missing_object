import pvporcupine
import pyaudio
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize Porcupine wake-word engine
porcupine = pvporcupine.create(
    access_key=os.getenv("access_key"),
    keywords=["blueberry"]
)
def get_next_audio_frame():
    # Define PyAudio parameters
    pa = pyaudio.PyAudio()
    sample_rate = 4000
    num_channels = 1
    audio_format = pyaudio.paInt16
    frame_length = 512

    # Open a PyAudio stream
    stream = pa.open(
        rate=sample_rate,
        channels=num_channels,
        format=audio_format,
        input=True,
        frames_per_buffer=frame_length
    )

    # Read a frame from the stream
    frame = np.frombuffer(stream.read(frame_length), dtype=np.int16)

    # Close the stream
    stream.stop_stream()
    stream.close()
    pa.terminate()

    return frame
    


while True:
  audio_frame = get_next_audio_frame()
  keyword_index = porcupine.process(audio_frame)
  print(keyword_index)
  if keyword_index == 0:
    print("Detected computer")
    break
    
porcupine.delete()

