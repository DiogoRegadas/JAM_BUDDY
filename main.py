from Models.Piano import Piano
from Models.Mix import Mix
from pynput import keyboard
import numpy as np
import pyaudio #portaudio.h installation error , fix:(brew install portaudio) (macOS)


def generate_sine_wave(ini ,end ,mix, CHUNKS_SAMPLE, mixed_chunk):

    # Create an array of time points from 0 to 'duration'
    # For 1 second at 44100Hz, this creates 44,100 evenly spaced numbers
    t = np.linspace(ini, end, CHUNKS_SAMPLE, endpoint=False, dtype=np.float32)


    #Calculate the sin wave math: sin(2 * pi * f * t)

    for frequency in mix.listMix:
        wave = np.sin(2 * np.pi * frequency * t)
        mixed_chunk += wave



    mixed_chunk = mixed_chunk / len(mix.listMix)
    # Convert the wave to 16 - bit audio format that sound cards expect
    # This scales our wave from (-1.0 to 1.0) to (-32768 to 32767)

    audio_data = (mixed_chunk * 32767).astype(np.int16)

    return audio_data.tobytes()


def on_press(key, inst, mix):
    try:
        if key.char in inst.NOTE_MAPPING:
            if inst.NOTE_MAPPING[key.char] not in mix.listMix:
                mix.AddNote(inst.NOTE_MAPPING[key.char])
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key, inst, mix):

    if key.char in inst.NOTE_MAPPING:
        if inst.NOTE_MAPPING[key.char] in mix.listMix:
            mix.removeNote(inst.NOTE_MAPPING[key.char])
    elif key == keyboard.Key.esc:
        # Stop listener
        return False


def main():

    m = Mix()
    piano = Piano()
    print(1)
    listener = keyboard.Listener(
            on_press=lambda event: on_press(event, piano, m),
            on_release=lambda event: on_release(event, piano, m))
    listener.start()

    print(2)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100,output=True)
    SAMPLE_RATE = 44100
    CHUNK_DURATION = 0.02
    CHUNK_SAMPLE = int(SAMPLE_RATE * CHUNK_DURATION)

    current_sample_index = 0

    try:
        while True:

            mixed_chunk = np.zeros(CHUNK_SAMPLE, dtype=np.float32)
            if len(m.listMix) > 0:

                ini_time = current_sample_index / SAMPLE_RATE
                end_time = (current_sample_index + CHUNK_SAMPLE) / SAMPLE_RATE

                audio_bytes = generate_sine_wave(ini_time, end_time, m, CHUNK_SAMPLE, mixed_chunk)

                stream.write(audio_bytes)

                current_sample_index += CHUNK_SAMPLE


    except KeyboardInterrupt:
        listener.stop()
        stream.stop_stream()
        stream.close()
        p.terminate()










if __name__ == '__main__':
    main()