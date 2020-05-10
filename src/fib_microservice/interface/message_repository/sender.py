from abc import ABC, abstractmethod


class ISender(ABC):
    """Abstract class for message queue sender"""

    def __init__(self, settings: "Settings"):
        self.settings = settings

    @abstractmethod
    async def send_message(self):
        pass

    @abstractmethod
    async def close(self):
        pass
