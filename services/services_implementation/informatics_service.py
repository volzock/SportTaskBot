import io

from services import ServiceAnswer
from services.services_implementation.base_service import BaseService


class InformaticsService(BaseService):
    netloc = "informatics.msk.ru"

    async def submit(self, url: str, file: io.BytesIO) -> ServiceAnswer:
        pass
