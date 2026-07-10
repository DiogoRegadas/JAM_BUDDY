import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from dataset_processor import MidiDataset
from model import MusicAI

def train_model():
    BATCH_SIZE = 16
    SEQUENCE_LENGTH = 8
    EPOCHS = 20
    LEARNING_RATE = 0.002

    dataset = MidiDataset("AI/midi_files", sequence_length=SEQUENCE_LENGTH)

    if len(dataset) == 0:
        print("Dataset is empty! Make sure you drop .mid files in 'AI/midi_files'!!")
        return

    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    model = MusicAI(vocab_size=128, embedding_dim=64, hidden_dim=128)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    print("Starting AI Training...")
    model.train()

    for epoch in range(EPOCHS):
        total_loss = 0
        for inputs, targets in dataloader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        average_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch + 1}/{EPOCHS} Average Error (Loss): {average_loss:4f}")

    torch.save(model.state_dict(), "piano_ai.pt")
    print("Training Complete! Saved model brain weights as 'piano_ai.pt'")

if __name__ == "__main__":
    train_model()