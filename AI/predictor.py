import torch
import torch.nn.functional as F
from AI.model import MusicAI
from AI.midi_freq import midi_to_freq

class AIPredictor:
    def __init__(self, model_path="piano_ai.pt", sequence_length=8):
        self.sequence_length = sequence_length
        self.model = MusicAI(vocab_size=128, embedding_dim=64, hidden_dim=128)

        try:
            self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
            print(f"Loaded model from '{model_path}'!")
        except FileNotFoundError:
            print(f"No model found at '{model_path}'!")

        self.model.eval()

        self.note_history = [60]*self.sequence_length

    def add_live_note(self, midi_note):

        self.note_history.append(midi_note)

        self.note_history = self.note_history[-self.sequence_length:]

    def predict_next_note(self, temperature=1.0):

        input_tensor = torch.tensor([self.note_history], dtype=torch.long)

        with torch.no_grad():

            logits = self.model(input_tensor)

            probabilities = F.softmax(logits, dim=-1)

            predicted_midi = torch.multinomial(probabilities[0], num_samples=1).item()

        predicted_freq = midi_to_freq(predicted_midi)

        return predicted_midi, predicted_freq
