# main.py
import pyaudio
import numpy as np
import time

# Internal imports from our new modular layout
from Models.Instr.Piano import Piano
from Models.Lists.Mix import Mix
from audio_engine import generate_sine_wave, remove_notes
from input_handler import start_keyboard_listener
from AI.predictor import AIPredictor


def main():
    m = Mix()
    piano = Piano()
    predictor = AIPredictor(model_path="piano_ai.pt")

    # Fire up the listener from our input module
    listener = start_keyboard_listener(piano, m, predictor)
    print("Keyboard listener started.")

    p = pyaudio.PyAudio()
    SAMPLE_RATE = 44100
    CHUNK_DURATION = 0.02
    CHUNK_SAMPLE = int(SAMPLE_RATE * CHUNK_DURATION)
    RELEASED_DURATION = 0.05

    stream = p.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, output=True)
    current_sample_index = 0

    print("Synthesizer running... Press SPACE to let your AI_JAM_BUDDY take over --or-- Ctrl+C to stop.")
    try:
        while True:
            mixed_chunk = np.zeros(CHUNK_SAMPLE, dtype=np.float32)

            if len(m.listMix) > 0:
                ini_time = current_sample_index / SAMPLE_RATE
                end_time = (current_sample_index + CHUNK_SAMPLE) / SAMPLE_RATE

                audio_bytes = generate_sine_wave(
                    ini_time, end_time, m, CHUNK_SAMPLE, mixed_chunk, RELEASED_DURATION
                )
                remove_notes(m, RELEASED_DURATION)
                stream.write(audio_bytes)
                current_sample_index += CHUNK_SAMPLE
            else:
                # If no notes are playing, sleep briefly to prevent 100% CPU usage
                time.sleep(0.005)

    except KeyboardInterrupt:
        print("\nShutting down cleanly...")
    finally:
        listener.stop()
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    main()