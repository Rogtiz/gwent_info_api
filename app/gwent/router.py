from fastapi import APIRouter, Depends
from app.gwent.utils import GwentAPI, GwentProfileParser

router = APIRouter()

api = GwentAPI()
profile_parser = GwentProfileParser()

@router.get("/user/{username}/id")
async def get_user_id(username: str):
    user_id = await api.get_user_id(username)
    if user_id:
        return {"user_id": user_id}
    return {"error": "User not found"}, 404


@router.get("/user/{user_id}/ranking/{season_id}")
async def get_ranking_info(user_id: str, season_id: str):
    ranking_info = await api.get_ranking_info(user_id, season_id)
    if ranking_info:
        return ranking_info
    return {"error": "Ranking information not found"}, 404


@router.get("/user/{user_id}/profile")
async def get_profile_data(user_id: str):
    profile_data = await api.get_profile_data(user_id)
    if profile_data:
        # return profile_parser.format_collection(profile_data.get("username"), profile_data)
        return profile_data
    return {"error": "Profile data not found"}, 404


