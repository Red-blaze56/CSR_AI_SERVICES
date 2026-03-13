from fastapi import FastAPI

from app.api.csr.router import csr_router

app = FastAPI(
    title="CSR_SERVICES_Navadrishti_API",
    description="API for CSR Services Navadrishti",
    version="v1",
)

app.include_router(router=csr_router, prefix="/api/v1")
#app.include_router(router=generate_campaign_router, prefix="/api/v1")
