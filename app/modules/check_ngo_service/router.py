from fastapi import APIRouter

from app.modules.check_ngo_service.schema import CheckNGOServicesRequest, CheckNGOServicesResponse
from app.modules.check_ngo_service.services import NGOServiceChecker

checker = NGOServiceChecker()

check_ngo_service_router = APIRouter(
    prefix="/check-ngo-service",
    tags=["Check NGO Service similar to CSR preferences"],
)

@check_ngo_service_router.post("/")
async def check_for_available_ngo_services(req: CheckNGOServicesRequest) -> CheckNGOServicesResponse:
    return await checker.check_ngo_services(req)

