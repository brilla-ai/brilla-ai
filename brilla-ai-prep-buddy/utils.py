import streamlit as st
import tempfile
import os
import pyaudio
import wave
import time

from api_clients import stt_client, tts_client

# Audio processing constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5


def autoplay_audio(audio_path: str, audio_place_holder) -> None:
    audio_place_holder.audio(audio_path, format="audio/wav", autoplay=True)


def transcribe_audio(audio_path: str, base_url: str) -> str:
    with st.spinner(f"Transcribing..."):
        transcript = stt_client.get_stt_transcript(audio_path, base_url)
    
    return transcript


def synthesize_audio(text: str, base_url: str) -> str:
    return tts_client.get_tts_audio(text, base_url)


def make_recording() -> str:
    audio = pyaudio.PyAudio()
    with st.spinner(f"Recording...\nYou have {RECORD_SECONDS} seconds to provide your answer"):
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


def simulate_riddle(qs: object,
                    riddle_id: int,
                    text_area: object,
                    transcript_box: object,
                    audio_place_holder: object,
                    base_url: str) -> int:
    if riddle_id > len(qs):
        st.error("Invalid Riddle ID")
    else:
        announce_start_file_path = synthesize_audio(text="Next Riddle", base_url=base_url)
        autoplay_audio(audio_path=announce_start_file_path, audio_place_holder=audio_place_holder)
        time.sleep(1.5)

        riddle = qs.get_next_riddle(riddle_id=riddle_id)
        if riddle is None:
            st.error("Couldn't fetch Riddle.")
        else:
            clues = riddle["clues"]
            groundtruths = riddle["answers"]
            content_to_display = ""

            for clue_num, clue in enumerate(clues, start=1):
                content_to_display += f"{clue_num}. {clue.strip()}\n"
                clue_audio_path = synthesize_audio(text=clue, base_url=base_url)
                autoplay_audio(audio_path=clue_audio_path, audio_place_holder=audio_place_holder)
                text_area.text_area(label="CLUES", value=content_to_display, height=300)
                delay_period = get_duration_of_audio(audio_path=clue_audio_path)
                time.sleep(delay_period)

            # Get user's answer
            user_answer_audio_path = make_recording()
            user_answer_transcript = transcribe_audio(audio_path=user_answer_audio_path, base_url=base_url).strip()
            transcript_box.text_area(label="Your Answer:", value=user_answer_transcript)

            answered_correctly = check_answer(groundtruths=groundtruths, user_answer=user_answer_transcript)
            if answered_correctly == True:
                autoplay_audio(audio_path=synthesize_audio(text="Yes, you are right.", base_url=base_url), audio_place_holder=audio_place_holder)
                score = 1
            else:
                autoplay_audio(audio_path=synthesize_audio(text="No, that is incorrect", base_url=base_url), audio_place_holder=audio_place_holder)
                score = 0

    return score


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
