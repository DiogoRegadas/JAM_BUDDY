import numpy as np

def freq_to_midi(frequency):
    """Turns a frequency like 261.63 into a MIDI integer like 60"""
    return int(round(69 + 12 * np.log2(frequency / 440.0)))

def midi_to_freq(midi_note):
    """Turns a MIDI integer like 88 into a frequency like 1318.51"""
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))