import torch
import torch.nn as nn

class MusicAI(nn.Module):
    def __init__(self, vocab_size=128, embedding_dim=64, hidden_dim=128):
        super(MusicAI, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim)

        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True, num_layers=2)

        self.fc = nn.Linear(hidden_dim, vocab_size)

    def forward(self, x):
        embendded = self.embedding(x)
        lstm_out, _ = self.lstm(embendded)

        last_note_output = lstm_out[:, -1, :]

        output_probability = self.fc(last_note_output)
        return output_probability
