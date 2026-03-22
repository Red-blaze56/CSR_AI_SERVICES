from app.modules.check_ngo_service.schema import CheckNGOServicesRequest, CheckNGOServicesResponse
from app.shared.embeddings.sentence_transformer import embed_text
from app.shared.embeddings.query_maker import make_query
from app.shared.clients.supabase_client import supabase
from src.config.settings import CONFIG 

class NGOServiceChecker:
    def __init__(self):
        pass

    async def get_query_embedding(self, payload: CheckNGOServicesRequest) -> list[float]:
        query = make_query(payload)
        return await embed_text(query)
    
    async def search_ngo_requests(self, embeddings: list[float], category: str, location: str, budget: float) -> list[dict]:
        result = await supabase.rpc("match_ngo_services", {
            "embedding": embeddings,
            "match_threshold": CONFIG.match_threshold,
            "match_count": CONFIG.match_count,
            "category": category,
            "location": location,
            "budget": budget
        })
        return result.data if result.data else []
    
    ## to make rpc function (match_ngo_response) in supabase

    async def check_ngo_services(self, payload: CheckNGOServicesRequest)->CheckNGOServicesResponse:
        embeddings = await self.get_query_embedding(payload)
        match_for_ngo = await self.search_ngo_requests(
            embeddings=embeddings,
            category=payload.category,
            location=payload.location,
            budget=payload.budget)
        if match_for_ngo:
            result =  CheckNGOServicesResponse(
                found=True,
                data=match_for_ngo,
                message="NGO service found matching the CSR preferences.",
            )

        return CheckNGOServicesResponse(
            found=False,
            data=None,
            message="No matching NGO service found for the given CSR preferences."
        )