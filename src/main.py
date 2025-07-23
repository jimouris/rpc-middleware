"""FastAPI middleware for rotating Ethereum JSON-RPC requests among multiple providers."""
import logging

import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from src.metrics import Metrics
from src.provider_pool import ProviderPool

app = FastAPI()

# Initialize provider pool and metrics
provider_pool = ProviderPool('rpc-providers/rpcs.csv')
metrics = Metrics()

logging.basicConfig(level=logging.INFO)

@app.post("/rpc")
async def rpc_proxy(request: Request):
    """Proxy JSON-RPC requests to a randomly selected provider and return the response."""
    try:
        body = await request.body()
        provider = provider_pool.get_random_provider()
        metrics.increment(provider.name)
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                provider.url,
                content=body,
                headers={"Content-Type": "application/json"}
            )
        return Response(
            content=resp.content,
            status_code=resp.status_code,
            media_type=resp.headers.get('content-type', 'application/json')
        )
    except httpx.RequestError as e:
        logging.error("Request error forwarding to provider %s: %s", provider.name, e)
        return JSONResponse(status_code=502, content={"error": "Bad gateway"})
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Unexpected error forwarding request: %s", e)
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.get("/metrics")
def get_metrics():
    """Return usage statistics for each provider."""
    return metrics.get_usage()
