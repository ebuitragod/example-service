import asyncio
import time
from datetime import datetime, timezone

from constants import SERVICES, Service
from fastapi import FastAPI

app = FastAPI(
    title="Local Service Status API", 
    version="0.1.0"
    )


async def probe_tcp(
    host: str,
    port: int
    ) -> tuple[bool, float]:
    started = time.perf_counter()
    try:
        _, writer = await asyncio.wait_for(
            asyncio.open_connection(
                host, 
                port
                ), 
            timeout=1.5
        )
        writer.close()
        await writer.wait_closed()
        return True, round((time.perf_counter() - started) * 1000, 2)
    except (OSError, asyncio.TimeoutError):
        return False, round((time.perf_counter() - started) * 1000, 2)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ports")
async def ports() -> dict[str, object]:
    async def inspect(service: Service) -> dict[str, object]:
        listening, latency_ms = await probe_tcp(service.name, service.port)
        return {
            "service": service.name,
            "target": f"{service.name}:{service.port}",
            "host_binding": f"127.0.0.1:{service.host_port}",
            "listening": listening,
            "latency_ms": latency_ms,
        }
    results = await asyncio.gather(*(inspect(service) for service in SERVICES))
    return {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "all_listening": all(result["listening"] for result in results),
        "services": results,
    }
