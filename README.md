# JAM_Buddy 🎹🤖

JAM_Buddy is a real-time, AI-powered musical collaborator. It listens to the live notes you play on your keyboard, processes your musical direction using a custom-trained Deep Learning model, and jams along with you in real-time when you hit the spacebar.

By leveraging multi-threaded concurrency, JAM_Buddy seamlessly interleaves predictive AI generation with a high-performance audio synthesis pipeline—completely eliminating latency and audio buffering artifacts.

---

## 🚀 Key Features

* **Custom Neural Network Architecture:** Built from scratch using PyTorch, utilizing custom Token Embeddings and stacked Long Short-Term Memory (LSTM) layers to capture complex musical context, harmony, and melodic momentum.
* **Intelligent Improvisation:** Features mathematical temperature controls to let you adjust the AI's creativity, allowing it to transition between rigid pattern adherence and highly expressive soloing.
* **Lag-Free Concurrency:** Implements a decoupled multi-threaded architecture where the AI "Composer" thread schedules notes ahead of time into a synchronized timeline queue, keeping the high-speed Audio Engine thread entirely unblocked.
* **Flexible Audio Synthesizer:** Fully native digital signal processing loop generating clean mathematical wave chunks at a precise granular `CHUNK_DURATION` of 20ms.

---

## 🧠 The AI Brain Architecture

The underlying core model (`MusicAI`) is designed specifically for temporal sequence tracking:

1.  **Embedding Layer:** Maps raw MIDI integers into a dense 64-dimensional harmonic vector space.
2.  **Stacked LSTM Layers:** A 128-hidden-unit recurring notepad architecture tracking sequential context window frames across an 8-note `SEQUENCE_LENGTH`.
3.  **Linear Output Layer:** Projects deep memory vectors back across a 128-key probability distribution representing every possible note on a full piano keyboard.

During training across classical repositories (e.g., Bach, Beethoven, Mozart), the optimization engine successfully reduced categorization loss error by **over 92%** (dropping from a baseline of `2.85` down to a highly accurate `0.22`).

---

## 🛠️ Project Structure

```text
JAM_Buddy/
├── AI/
│   ├── model.py            # PyTorch Neural Network definition (LSTM)
│   ├── train.py            # Mathematical training & backpropagation loop
│   ├── predictor.py        # Inference engine & probabilistic sampler
│   ├── helpers.py          # Data utilities (e.g., MIDI-to-Frequency mapping)
│   └── midi_files/         # Your raw MIDI data library directory
├── Tests/
│   └── predicted_Test.py   # Simulation verification script
├── activate_Jam_Buddy.py   # Asynchronous multi-threading thread manager
├── main.py                 # Core entry point and real-time audio loop
└── piano_ai.pt             # The frozen serialized model binary weights 🧠
