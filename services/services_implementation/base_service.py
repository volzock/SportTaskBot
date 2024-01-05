import io
from abc import ABC, abstractmethod

from services import ServiceAnswer


class BaseService(ABC):
    netloc: str

    @abstractmethod
    async def submit(self, url: str, file: io.BytesIO) -> ServiceAnswer:
        pass
