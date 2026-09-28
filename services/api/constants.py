

import os

from pydantic import BaseModel


class Service(BaseModel):
    name: str
    port: int
    host_port: int | None = None


SERVICES: tuple[Service, ...] = (
    Service(
        name="web", 
        port=8080, 
        host_port=int(os.getenv("WEB_HOST_PORT", "8080"))
    ),
    Service(
        name="whoami",
        port=80,
        host_port=8081
        ),
    Service(
        name="echo", 
        port=5678, 
        host_port=8082
    ),
    Service(
        name="static-example", 
        port=8080, 
        host_port=8083
    ),
    Service(
        name="ssh", 
        port=2222, 
        host_port=2222
    ),
    Service(
        name="api", 
        port=8000, 
        host_port=8084
    ),
)



