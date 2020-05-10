from abc import ABC, abstractmethod


class IDatabaseRepository(ABC):
    def __init__(self, settings: "Settings"):
        self.settings = settings

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def save_number(self):
        pass
