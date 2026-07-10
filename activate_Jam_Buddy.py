import threading
import time

ai_jamming = False

def start_jam_buddy(predictor, mix):
    global ai_jamming
    print("Starting JAM Buddy...")

    while ai_jamming:

        next_midi, next_freq = predictor.predict_next_note(temperature=0.8)
        next_note = {
            "freq": next_freq,
            "start_t": time.time(),
            "release_t": (time.time() + 0.5),
        }
        mix.addNote(next_note)
        predictor.add_live_note(next_midi)

        time.sleep(0.45)

def on_spacebar_pressed(predictor, mix):
    global ai_jamming

    if not ai_jamming:
        ai_jamming = True

        threading.Thread(target=start_jam_buddy, args=(predictor, mix), daemon=True).start()
    else:
        ai_jamming = False
        print("AI JAM Buddy Stopped.")