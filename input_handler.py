# input_handler.py
import time
from pynput import keyboard
from AI.midi_freq import freq_to_midi
import activate_Jam_Buddy as jm


def on_press(key, inst, mix, predictor):
    try:
        if hasattr(key, 'char') and key.char in inst.NOTE_MAPPING:
            if not any(n["freq"] == inst.NOTE_MAPPING[key.char] for n in mix.listMix):
                new_note = {
                    "freq": inst.NOTE_MAPPING[key.char],
                    "start_t": time.time(),
                    "release_t": None
                }
                mix.addNote(new_note)
                midi_note=freq_to_midi(new_note["freq"])
                predictor.add_live_note(midi_note)
        elif key.space:
            jm.on_spacebar_pressed(predictor, mix)
    except AttributeError:
        print(f'Special key {key} pressed')


def on_release(key, inst, mix):
    try:
        if hasattr(key, 'char') and key.char in inst.NOTE_MAPPING:
            for note in mix.listMix:
                if note["freq"] == inst.NOTE_MAPPING[key.char] and note["release_t"] is None:
                    note["release_t"] = time.time()
    except AttributeError:
        pass


def start_keyboard_listener(inst, mix, predictor):
    """Sets up and starts the background keyboard listener thread"""
    listener = keyboard.Listener(
        on_press=lambda event: on_press(event, inst, mix, predictor),
        on_release=lambda event: on_release(event, inst, mix)
    )
    listener.start()
    return listener
