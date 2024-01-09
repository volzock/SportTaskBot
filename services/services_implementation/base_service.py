import io
import re
from abc import ABC, abstractmethod
from typing import Tuple

from bs4 import BeautifulSoup
from requests import Session
from sqlalchemy import select, ScalarResult
from sqlalchemy.orm import Session as SqlSession

from services import ServiceAnswer
from utils import Singleton
from database import Service, ServiceData, db


class BaseService(ABC):
    netloc: str

    def _get_data(self) -> ScalarResult:
        with SqlSession(db) as session:
            with session.begin():
                stmt = select(Service).where(Service.url == self.netloc)
                service = session.scalars(stmt).one_or_none()

                if service is None:
                    raise RuntimeError(f"You need to setup service for Classname={self.__class__.__name__}")

                stmt = select(ServiceData).where(service_id=service.id)
                services_data = session.scalars(stmt)

                return services_data

    def _get_single_data(self) -> Tuple[str, str]:
        with SqlSession(db) as session:
            with session.begin():
                services_data = self._get_data().one_or_none()

                if services_data is None:
                    raise RuntimeError(f"You need to setup service_data for Classname={self.__class__.__name__}")

                return services_data.login, services_data.password

    @abstractmethod
    async def submit(self, url: str, file: io.BytesIO) -> ServiceAnswer:
        pass
