# dataset_processor.py
import os
import mido
import torch
from torch.utils.data import Dataset, DataLoader


class MidiDataset(Dataset):
    def __init__(self, midi_folder, sequence_length=8):
        self.sequence_length = sequence_length
        self.all_notes = []

        # 1. Read every MIDI file in the target folder
        if not os.path.exists(midi_folder):
            os.makedirs(midi_folder)
            print(f"Created '{midi_folder}' directory. Please drop your MIDI files (.mid) inside it!")
            return

        for file in os.listdir(midi_folder):
            if file.endswith('.mid') or file.endswith('.midi'):
                file_path = os.path.join(midi_folder, file)
                try:
                    self.all_notes.extend(self._extract_notes(file_path))
                except Exception as e:
                    print(f"Skipping corrupt file {file}: {e}")

        print(f"Total musical notes extracted for training: {len(self.all_notes)}")

    def _extract_notes(self, file_path):
        """Extracts raw MIDI note values sequentially from a single MIDI file"""
        notes = []
        mid = mido.MidiFile(file_path)

        # We look through all tracks inside the MIDI file
        for track in mid.tracks:
            for msg in track:
                # We only care about message packets telling a note to start playing
                # velocity > 0 means the note is actively sounding
                if msg.type == 'note_on' and msg.velocity > 0:
                    # Guaranteeing the note fits within standard 0-127 MIDI limits
                    if 0 <= msg.note <= 127:
                        notes.append(msg.note)
        return notes

    def __len__(self):
        # The total number of valid sliding windows we can extract
        if len(self.all_notes) <= self.sequence_length:
            return 0
        return len(self.all_notes) - self.sequence_length

    def __getitem__(self, idx):
        # Extract the sequence of inputs (X) and the single next note target (Y)
        x = self.all_notes[idx: idx + self.sequence_length]
        y = self.all_notes[idx + self.sequence_length]

        return torch.tensor(x, dtype=torch.long), torch.tensor(y, dtype=torch.long)