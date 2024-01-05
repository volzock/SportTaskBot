from typing import Dict

import services.services_implementation as services


class ServiceSelector:
    services: Dict[str, services.BaseService]

    def __init__(self):
        self.services = dict()

        for name in dir(services):
            probably_service = getattr(services, name)
            if isinstance(services.BaseService, type(probably_service)) and services.BaseService != probably_service:
                self.services[probably_service.netloc] = probably_service

    def __getitem__(self, item):
        if item not in self.services:
            raise KeyError
        return self.services[item]
