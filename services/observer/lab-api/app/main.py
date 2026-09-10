from fastapi import FastAPI, Response
import asyncio 

app = FastAPI(title="AGEGIS Failure Lab")

@app.get("/health")
def health():
    return{"status": "alive"}

@app.get("/ready")
def ready():
    return{"status": "ready"}

@app.get("/simulate/error")
def simulate_error(response: Response):
    response.status_code = 500
    return {
        "status": "error",
        "message": "Simulated internal server error",
    }

@app.get("/simulate/latency")
async def simulate_latency(seconds: int = 3):
    await asyncio.sleep(seconds)

    return {
        "status": "completed",
        "delay_seconds": seconds,
    }