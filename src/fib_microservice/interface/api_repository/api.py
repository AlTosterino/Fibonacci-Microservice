from abc import ABC, abstractmethod


class IAPIRepository(ABC):
    def __init__(self, settings: "Settings"):
        self.settings = settings
