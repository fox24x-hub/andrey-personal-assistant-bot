from collections import defaultdict
from typing import Optional


class MemoryService:
    """Service for managing user conversation history."""

    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.user_history = defaultdict(list)

    def add_message(self, user_id: int, role: str, content: str):
        """Add message to user's history."""
        self.user_history[user_id].append({
            "role": role,
            "content": content
        })

        # Keep only last max_history messages
        if len(self.user_history[user_id]) > self.max_history 
            self.user_history[user_id] = self.user_history[user_id][-self.max_history :]

    def get_history(self, user_id: int) -> list:
        """Get user's conversation history."""
        return self.user_history.get(user_id, [])

    def clear_history(self, user_id: int):
        """Clear user's history."""
        if user_id in self.user_history:
            del self.user_history[user_id]
