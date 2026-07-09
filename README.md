# JAM_Buddy 🎹🤖

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An asynchronous, real-time AI musical accompaniment engine. JAM_Buddy listens to live user input, updates a rolling context window, and utilizes a custom-trained Deep Learning model to synthesize complementary improvisations dynamically upon triggering.

By decoupling the deep learning inference from the core audio pipeline via a multi-threaded architecture, the system guarantees low-latency, glitch-free audio processing at a granular 20ms chunk scale.

---

## 🚀 System Architecture & Pipeline

JAM_Buddy is split into two distinct, isolated operational loops running on separate CPU execution threads to preserve audio buffer integrity:

1.  **The Audio Synthesis Thread (High Priority):** Continuously renders digital signal processing (DSP) wave chunks every `0.02 seconds` (20ms). It evaluates a shared thread-safe timeline queue (`mix`) to mix and output valid active frequencies.
2.  **The Predictive Inference Thread (Background):** Wakes up via a timed metronome step. It evaluates the user's recent input history tensor, performs a forward pass through the model, and appends time-forged note event dictionaries directly into the shared timeline.

```text
  [ User MIDI Input ] ──► [ 8-Step History Buffer ]
                                  │
                                  ▼
                        [ AI Inference Thread ]
                        ┌───────────────────┐
                        │ Forward Pass      │
                        │ Prob Sampler      │ ──► [ Time-Forged Note Event ]
                        └───────────────────┘                 │
                                                              ▼
 [ Audio Out ] ◄── [ 20ms DSP Chunk Render ] ◄── Read ── [ Shared Mix Timeline ]
