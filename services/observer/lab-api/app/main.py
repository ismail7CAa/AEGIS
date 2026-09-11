import asyncio

from fastapi import FastAPI, Response

app = FastAPI(title="AEGIS Failure Lab")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready"}


@app.get("/simulate/error")
def simulate_error(response: Response) -> dict[str, str]:
    response.status_code = 500

    return {
        "status": "error",
        "message": "Simulated internal server error",
    }


@app.get("/simulate/latency")
async def simulate_latency(seconds: int = 3) -> dict[str, str | int]:
    await asyncio.sleep(seconds)

    return {
        "status": "completed",
        "delay_seconds": seconds,
    }