import customtkinter as ctk
import threading
from queue import Queue
import os

from question_service import QuestionService
from utils import synthesize_audio, autoplay_audio, make_recording, transcribe_audio

question_service = QuestionService()
BASE_URL = "https://a96c-34-66-250-97.ngrok-free.app/"

class App:

    def __init__(self, root):
        self.root = root
        self.is_running = threading.Event()
        self.is_attempting = threading.Event()

        self.start_button = ctk.CTkButton(master=root, text="Start Assessment", command=self.start_assessment)
        self.start_button.pack(pady=20)

        self.answer_button = ctk.CTkButton(master=root, text="Make Attempt", command=self.make_attempt)
        self.answer_button.pack(pady=20)

        self.spinner_label = ctk.CTkLabel(master=root, text="Assessment Ongoing...", text_color="green")
        self.spinner_label.pack(pady=20)
        self.spinner_label.pack_forget()  # Hide the spinner initially

        self.processing_answer_label = ctk.CTkLabel(master=root, text="", text_color="blue")
        self.processing_answer_label.pack(pady=20)
        self.processing_answer_label.pack_forget()

        self.riddle_label = ctk.CTkLabel(master=root, text="Riddle: 0/0")
        self.riddle_label.pack(pady=10)

        self.score_label = ctk.CTkLabel(master=root, text="Score: 0")
        self.score_label.pack(pady=10)

        self.worker_thread = None
        self.current_riddle_id = 1
        self.total_riddles = len(question_service)
        self.score = 0
        self.audio_queue = Queue()

        self.remaining_clues = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_labels(self):
        self.riddle_label.configure(text=f"Riddle: {self.current_riddle_id}/{self.total_riddles}")
        self.score_label.configure(text=f"Score: {self.score}")

    def start_assessment(self):
        if self.worker_thread and self.worker_thread.is_alive():
            # Assessment is already running.
            return

        self.spinner_label.pack(pady=20)  # Show the spinner
        self.worker_thread = threading.Thread(target=self.assessment_simulation)
        self.worker_thread.start()

        # Change the text to "Next Riddle" after starting the first assessment
        if self.current_riddle_id == 1:
            self.start_button.configure(text="Next Riddle")

    def assessment_simulation(self):
        self.process_riddle()
        self.spinner_label.pack_forget()  # Hide the spinner after assessment is done

    def process_riddle(self):
        self.update_labels()

        if self.current_riddle_id == 1:
            autoplay_audio(audio_path="cache/round_rules.wav")
        
        autoplay_audio(audio_path=f"cache/riddle_{self.current_riddle_id}.wav")
        riddle = question_service.get_next_riddle(self.current_riddle_id)
        clues = riddle["clues"]

        self.is_running.set()  # Allow processing for the new riddle

        for clue_num, clue in enumerate(clues, start=1):
            clue_audio_path = synthesize_audio(text=clue.strip().lower(), base_url=BASE_URL)
            print(f"Processing Clue {clue_num}")
            autoplay_audio(audio_path=clue_audio_path)

            # Prefetch the next clue's audio if it exists
            #if clue_num < len(clues):
            #    threading.Thread(target=self.synthesize_and_queue_audio, args=(clues[clue_num].strip(),)).start()

            # Check if the user wants to make an attempt
            if self.is_attempting.is_set():
                self.remaining_clues = clues[clue_num+1:]
                self.handle_attempt(clue_num)
                self.is_attempting.clear()
                break

        self.is_running.clear()
        if not self.is_attempting.is_set():  # If an attempt was not made, move to the next riddle
            self.current_riddle_id += 1 if self.current_riddle_id < len(question_service) else 1
        

    def synthesize_and_queue_audio(self, text):
        clue_audio_path = synthesize_audio(text=text, base_url=BASE_URL)
        self.audio_queue.put(clue_audio_path)

    def make_attempt(self):
        if self.is_running.is_set():
            self.is_attempting.set()

    def handle_attempt(self, clue_num):
        self.processing_answer_label.configure(text="Recording Answer. You have 5 seconds to provide your answer...")
        self.processing_answer_label.pack(pady=20)  # Show the processing label
        
        answer_audio_path = make_recording()
        autoplay_audio(answer_audio_path)
        
        self.processing_answer_label.configure(text="Processing Your Answer...")
        user_answer = transcribe_audio(audio_path=answer_audio_path, base_url=BASE_URL)
        
        riddle = question_service.get_next_riddle(self.current_riddle_id)
        groundtruths = riddle["answers"]
        
        if self.check_answer(user_answer, groundtruths) == True:
            autoplay_audio(audio_path="./cache/correct.wav")
            if clue_num == 1:
                self.score += 5
                annon_audio_path = synthesize_audio(text="I was on the first clue, five points.", base_url=BASE_URL)
                autoplay_audio(annon_audio_path)
            elif clue_num == 2:
                self.score += 4
                annon_audio_path = synthesize_audio(text="I was on the second clue, four points.", base_url=BASE_URL)
                autoplay_audio(annon_audio_path)
            else:
                self.score += 3
                if clue_num == 3:
                    suffix = "rd"
                else:
                    suffix = "th"
                    annon_audio_path = synthesize_audio(text=f"I was on the {clue_num}{suffix} clue, three points.", base_url=BASE_URL)
                autoplay_audio(annon_audio_path)
        else:
            autoplay_audio(audio_path="./cache/incorrect.wav")

            # Prompt the user that you will be reading the remaining clues
            if len(self.remaining_clues) >=1:
                prompt_audio_path = synthesize_audio(text="Now I continue with the clues.", base_url=BASE_URL)
                autoplay_audio(audio_path=prompt_audio_path)

                for clue in self.remaining_clues:
                    clue_audio_path = synthesize_audio(text=clue, base_url=BASE_URL)
                    autoplay_audio(clue_audio_path)
            
            expected_answer_audio_path = synthesize_audio(f"The answer I was expecting is {groundtruths[0]}", base_url=BASE_URL)
            autoplay_audio(expected_answer_audio_path)

        self.update_labels()
        self.processing_answer_label.pack_forget()  # Hide the processing label

    def check_answer(self, user_answer, groundtruths):
        if any(user_answer.lower().strip().replace('.', '') == answer.lower().strip() for answer in groundtruths):
            return True
        return False

    def go_to_next_riddle(self):
        self.current_riddle_id += 1
        if self.current_riddle_id <= self.total_riddles:
            self.start_assessment()  # Start the assessment for the next riddle
        else:
            self.start_button.configure(text="Start Assessment")
            self.current_riddle_id = 1

    def on_closing(self):
        self.root.destroy()
        os._exit(0)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("600x400")
    app = App(root)
    root.mainloop()
