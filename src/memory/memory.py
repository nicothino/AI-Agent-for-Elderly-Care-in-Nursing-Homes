"""
Memory module - abstractions for short-term and long-term memory
- Short-term: recent messages (RAM)
- Long-term: embeddings saved to vector DB via vector_store
"""
class ShortTermMemory:
    def __init__(self, max_turns=5):
        self.max_turns = max_turns
        self.buffer = []

    def add(self, role, text):
        self.buffer.append({"role": role, "text": text})
        if len(self.buffer) > self.max_turns:
            self.buffer.pop(0)

    def get(self):
        return self.buffer
