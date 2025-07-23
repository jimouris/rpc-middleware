import logging
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
import httpx

from src.provider_pool import ProviderPool
from src.metrics import Metrics

app = FastAPI()

# Initialize provider pool and metrics
provider_pool = ProviderPool('rpc-providers/rpcs.csv')
metrics = Metrics()

logging.basicConfig(level=logging.INFO)

@app.post("/rpc")
async def rpc_proxy(request: Request):
    try:
        body = await request.body()
        provider = provider_pool.get_random_provider()
        metrics.increment(provider.name)
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(provider.url, content=body, headers={"Content-Type": "application/json"})
        return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get('content-type', 'application/json'))
    except Exception as e:
        logging.error(f"Error forwarding request: {e}")
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.get("/metrics")
def get_metrics():
    return metrics.get_usage()
