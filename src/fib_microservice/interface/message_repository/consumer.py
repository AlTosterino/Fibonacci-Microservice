from abc import ABC, abstractmethod


class IConsumer(ABC):
    """Abstract class for message queue consumer"""

    def __init__(self, settings: "Settings"):
        self.settings = settings

    @abstractmethod
    async def on_message(self):
        pass

    @abstractmethod
    async def listen(self):
        pass

    @abstractmethod
    async def close(self):
        pass
