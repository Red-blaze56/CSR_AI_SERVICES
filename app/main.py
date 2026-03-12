from fastapi import FastAPI

from api.csr import router

app = FastAPI(
    title="CSR_SERVICES_Navadrishti_API",
    description="API for CSR Services Navadrishti",
    version="v1",
)

app.include_router(router=router)