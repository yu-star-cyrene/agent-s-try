from abc import ABC, abstractmethod


class ModelClient(ABC):
    @abstractmethod
    def inspect(self, prompt: str, image_path: str | None = None) -> str:
        raise NotImplementedError
