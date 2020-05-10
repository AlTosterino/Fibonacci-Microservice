from abc import ABC, abstractmethod


class IAPIRepository(ABC):  # pragma: no cover
    def __init__(self, settings: "Settings"):
        self.settings = settings
