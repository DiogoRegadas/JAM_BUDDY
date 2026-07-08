# audio_engine.py
import numpy as np
import time

def generate_sine_wave(ini, end, mix, CHUNKS_SAMPLE, mixed_chunk, RELEASED_DURATION):
    t = np.linspace(ini, end, CHUNKS_SAMPLE, endpoint=False, dtype=np.float32)

    for frequency in mix.listMix:
        freq_ajust = np.sqrt(frequency["freq"] / 261.63)

        f1 = (0.5 * freq_ajust) * np.sin(2 * np.pi * frequency["freq"] * t)
        f2 = (0.3 * freq_ajust) * np.sin(2 * np.pi * (frequency["freq"] * 2) * t)
        f3 = (0.2 * freq_ajust) * np.sin(2 * np.pi * (frequency["freq"] * 3) * t)

        harmonics_wave = f1 + f2 + f3
        envelope = np.ones_like(t)

        if frequency["release_t"] is not None:
            time_since_release = t - frequency["release_t"]
            fade_factor = 1.0 - (time_since_release / RELEASED_DURATION)
            fade_factor = np.clip(fade_factor, 0.0, 1.0)
            envelope *= fade_factor

        mixed_chunk += harmonics_wave * envelope

    if len(mix.listMix) > 0:
        mixed_chunk = mixed_chunk / len(mix.listMix)

    mixed_chunk = np.tanh(mixed_chunk)
    audio_data = (mixed_chunk * 32767).astype(np.int16)
    return audio_data.tobytes()


def remove_notes(mix, RELEASED_DURATION):
    now = time.time()
    notes_removed = []
    for note in mix.listMix:
        if note["release_t"] is not None and (now - note["release_t"]) > RELEASED_DURATION:
            notes_removed.append(note)

    for note in notes_removed:
        mix.removeNote(note)