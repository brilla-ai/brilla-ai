import tempfile
import os
import pyaudio
import wave
import time
from pydub import AudioSegment
from pydub.playback import play

from api_clients import stt_client, tts_client

# Audio processing constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2.5


def autoplay_audio(audio_path: str) -> None:
    audio = AudioSegment.from_file(audio_path)
    play(audio)


def transcribe_audio(audio_path: str, base_url: str) -> str:
    return stt_client.get_stt_transcript(audio_path, base_url)


def synthesize_audio(text: str, base_url: str) -> str:
    return tts_client.get_tts_audio(text, base_url)


def make_recording() -> str:
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []
    for _ in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    
    audio.terminate()
    
    tempdir = tempfile.mkdtemp()
    file_path = os.path.join(tempdir, "recorded_audio.wav")
    with wave.open(file_path, "wb") as f:
        f.setnchannels(CHANNELS)
        f.setsampwidth(audio.get_sample_size(FORMAT))
        f.setframerate(RATE)
        f.writeframes(b"".join(frames))

    return file_path


def get_duration_of_audio(audio_path: str) -> int:
    with wave.open(audio_path, "rb") as f:
        num_frames = f.getnframes()
        frame_rate = f.getframerate()

        duration_seconds = num_frames / float(frame_rate)

    return duration_seconds


def check_answer(groundtruths: list[str], user_answer: str):
    return any(user_answer.lower() == groundtruth.lower() for groundtruth in groundtruths)


class SessionState:
    def __init__(self):
        self.state_dir = "./state-docs"
        if not os.path.exists(self.state_dir):
            os.mkdir(self.state_dir)

        self.state_doc = os.path.join(self.state_dir, "previous_state_doc.txt")
        try:
            with open(self.state_doc, "r", encoding="utf-8") as f:
                # riddle_id\nscore
                lines = f.readlines()
                self.riddle_id = int(lines[0])
                self.score = int(lines[1])
        except:
            self.riddle_id = 1
            self.score = 0

    def write_state(self, riddle_id, score):
        with open(self.state_doc, 'w', encoding="utf-8") as f:
            f.write(f"{riddle_id}\n")
            f.write(f"{score}")
