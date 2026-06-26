from Models.Piano import Piano
from pynput import keyboard
import numpy as np
import pyaudio #portaudio.h installation error , fix:(brew install portaudio) (macOS)


def generate_sine_wave(frequency, sample_rate= 44100, duration = 1):

    # Create an array of time points from 0 to 'duration'
    # For 1 second at 44100Hz, this creates 44,100 evenly spaced numbers
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)


    #Calculate the sin wave math: sin(2 * pi * f * t)

    wave = np.sin(2 * np.pi * frequency * t)


    # Convert the wave to 16 - bit audio format that sound cards expect
    # This scales our wave from (-1.0 to 1.0) to (-32768 to 32767)

    audio_data = (wave * 32767).astype(np.int16)

    return audio_data.tobytes()

def play_sound(audio_data, stream):
    stream.write(audio_data)




def on_press(key, inst, stream):
    try:
        if key.char in inst.NOTE_MAPPING:
            print(key.char)
            sound_wave = generate_sine_wave(inst.NOTE_MAPPING[key.char])
            play_sound(sound_wave, stream)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))


def on_release(key, stream):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100,output=True)

    piano = Piano()
    print(piano.NOTE_MAPPING)
    with keyboard.Listener(
            on_press = lambda event: on_press(event, piano, stream),
            on_release= lambda event: on_release(event,stream)) as listener:
        listener.join()

    stream.stop_stream()
    stream.close()
    p.terminate()







if __name__ == '__main__':
    main()