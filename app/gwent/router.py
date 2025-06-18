from fastapi import APIRouter, Depends, HTTPException
from app.gwent.utils import GwentAPI, GwentProfileParser, GwentSiteParser
from app.gwent.schemas import FullUserRankingInfoSchema, FullProfileDataSchema, GwentSitePlayerInfoSchema, RanksThresholdSchema

router = APIRouter()

api = GwentAPI()
profile_parser = GwentProfileParser()
site_parser = GwentSiteParser()

@router.get("/user/{username}/id")
async def get_user_id(username: str):
    user_id = await api.get_user_id(username)
    if user_id:
        return {"user_id": user_id}
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/user/{user_id}/ranking/{season_id}")
async def get_ranking_info(user_id: str, season_id: str) -> FullUserRankingInfoSchema:
    ranking_info = await api.get_ranking_info(user_id, season_id)
    if ranking_info:
        return ranking_info
    raise HTTPException(status_code=404, detail="Ranking information not found")


@router.get("/user/{user_id}/profile")
async def get_profile_data(user_id: str) -> FullProfileDataSchema:
    profile_data = await api.get_profile_data(user_id)
    if profile_data:
        # return profile_parser.format_collection(profile_data.get("username"), profile_data)
        return profile_data
    raise HTTPException(status_code=404, detail="Profile data not found")


@router.get("/get_threshold_of_ranks")
async def get_threshold_of_ranks() -> RanksThresholdSchema:
    thresholds = site_parser.get_mmr_threshold_of_ranks()
    if thresholds:
        return thresholds
    raise HTTPException(status_code=404, detail="Thresholds not found")


@router.get("/get_username_by_place/{place}")
async def get_username_by_place(place: int) -> GwentSitePlayerInfoSchema:
    username = site_parser.get_mmr_threshold(place)
    if username:
        return username
    raise HTTPException(status_code=404, detail="Username not found")


@router.get("/get_top_players")
async def get_top_players(page: int = 1) -> list[GwentSitePlayerInfoSchema]:
    top_players = site_parser.get_top_ranks(page)
    if top_players:
        return top_players
    raise HTTPException(status_code=404, detail="Top players not found")
