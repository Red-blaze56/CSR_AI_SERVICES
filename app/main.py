from fastapi import FastAPI

from app.api.csr.router import csr_router
from app.api.campaigns.router import campaigns_router

app = FastAPI(
    title="CSR_SERVICES_Navadrishti_API",
    description="API for CSR Services Navadrishti",
    version="v1",
)

app.include_router(router=csr_router, prefix="/api/{version}")
app.include_router(router=campaigns_router, prefix="/api/{version}")
