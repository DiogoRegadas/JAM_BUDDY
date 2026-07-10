from AI.predictor import AIPredictor

if __name__ == "__main__":
    # Test simulation
    predictor = AIPredictor(model_path="piano_ai.pt")

    # Simulate you playing a basic C Major scale up
    user_played = [60, 62, 64, 65, 67, 69, 71, 72]
    print(f"\nSimulating user playing: {user_played}")

    for note in user_played:
        predictor.add_live_note(note)

    # Ask the AI to predict the next 5 notes in a row!
    print("\nAI is thinking about what should come next...")
    for i in range(5):
        next_midi, next_freq = predictor.predict_next_note(temperature=0.8)
        print(f"Prediction {i + 1}: AI chose MIDI Note {next_midi} (Frequency: {next_freq:.2f} Hz)")

        # Feed the AI's own prediction back into its history so it can chain ideas!
        predictor.add_live_note(next_midi)