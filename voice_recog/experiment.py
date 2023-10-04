import pvporcupine
import pyaudio
import numpy as np
import cv2
import threading
from dotenv import load_dotenv
import os

load_dotenv()

print(os.environ["ACCESS_KEY"])
porcupine = pvporcupine.create(
    access_key=os.environ["ACCESS_KEY"],
    keywords=["computer"]
)

cap = cv2.VideoCapture(0)
audio = pyaudio.PyAudio()

FRAMES_PER_BUFFER = 512
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=FRAMES_PER_BUFFER)

stop_threads = threading.Event()

def get_video(cap, stop_threads):
    while not stop_threads.is_set():
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or stop_threads.is_set():
            break

def get_audio(stream, audio, stop_threads):
    while not stop_threads.is_set():
        data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
        audio_frame = np.frombuffer(data, dtype=np.int16)
        keyword_index = porcupine.process(audio_frame)
        print(keyword_index)
        if keyword_index == 0:
            print("Detected computer")
            stop_threads.set()

video_thread = threading.Thread(target=get_video, args=(cap, stop_threads))
audio_thread = threading.Thread(target=get_audio, args=(stream, audio, stop_threads))

# video_thread.start()
audio_thread.start()

try:
    while not stop_threads.is_set():
        pass
except KeyboardInterrupt:
    print("Ctrl+C detected, stopping threads...")
    stop_threads.set()

# video_thread.join()
audio_thread.join()

print("done!")
porcupine.delete()
cap.release()
cv2.destroyAllWindows()
