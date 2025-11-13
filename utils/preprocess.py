# utils/processor.py
from collections import deque

class SignProcessor:
    def __init__(self, buffer_size=12):
        self.buffer = deque(maxlen=buffer_size)
        self.sentence = []

    def update(self, prediction):
        """
        Smooths prediction noise using buffer majority vote.
        """
        self.buffer.append(prediction)

        # Not enough frames to get stable output yet
        if len(self.buffer) < self.buffer.maxlen:
            return None, " ".join(self.sentence)

        # Get the most repeated value in buffer
        stable_pred = max(set(self.buffer), key=self.buffer.count)

        # Only add if different from last word to prevent spam
        if len(self.sentence) == 0 or self.sentence[-1] != stable_pred:
            self.sentence.append(stable_pred)

        return stable_pred, " ".join(self.sentence)

    def clear_sentence(self):
        self.sentence = []
        self.buffer.clear()

    def export_sentence(self, filename="translation.txt"):
        """
        Exports the current sentence to a text file.
        """
        with open(filename, "w") as f:
            f.write(" ".join(self.sentence))
        print(f"Sentence exported to {filename}")
