from typing import Optional
from pydantic import BaseModel, Field, RootModel


class RankingInfoRankProgressionSchema(BaseModel):
    mosaic_piece_count: int
    rank: int


class FactionProgressionsItemSchema(BaseModel):
    is_used_for_score_calculation: bool
    unlocked_score: int
    real_score: int
    real_score_peak: int
    games_count: int
    unlocked_score_games_count_threshold: int
    unlocked_score_fraction: float



class RankingInfoFactionProgressionsSchema(BaseModel):
    faction: str
    faction_progression: FactionProgressionsItemSchema


class FactionGamesStatsItemSchema(BaseModel):
    wins_count: int
    losses_count: int
    draws_count: int
    games_count: int


class RankingInfoFactionGamesStatsSchema(BaseModel):
    faction: str
    faction_games_stats: FactionGamesStatsItemSchema


class RankingInfoRatingSchema(BaseModel):
    score: int


class RankingInfoParagonSchema(BaseModel):
    paragon_level: int
    player_level: int


class RankingInfoRequirementParamsSchema(BaseModel):
    status: str


class RankingInfoRequirementSchema(BaseModel):
    type: str
    params: RankingInfoRequirementParamsSchema


class RankingInfoVanitySchema(BaseModel):
    category: str
    item_definition_id: str


class FullUserRankingInfoSchema(BaseModel):
    id: str
    username: str
    platform: str
    title: str
    score: int
    position: int
    continental_position: int
    rank_id: int
    leaderboard: str
    data_score_updated: Optional[str] = None
    data_level_updated: Optional[str] = None
    date_created: str
    wins_count: int
    losses_count: int
    draws_count: int
    games_count: int
    level: int
    continent: str
    country: str
    rank_progression: RankingInfoRankProgressionSchema
    faction_progressions: list[RankingInfoFactionProgressionsSchema]
    faction_games_stats: list[RankingInfoFactionGamesStatsSchema]
    rating: RankingInfoRatingSchema
    paragon: RankingInfoParagonSchema
    requirements: list[RankingInfoRequirementSchema]
    vanity: list[RankingInfoVanitySchema] | None = None


class ProfileDataProgressBarSchema(BaseModel):
    level: int
    crown_pieces: int


class ProfileDataAccomplishmentSchema(BaseModel):
    id: str
    type: str


class ProfileDataStatsWinsSchema(BaseModel):
    Monster: int
    Nilfgaard: int
    NorthernKingdom: int
    Scoiatael: int
    Skellige: int
    Syndicate: int


class ProfileDataStatsSchema(BaseModel):
    wins: ProfileDataStatsWinsSchema
    ggs_sent_count: int
    ggs_received_count: int
    pro_ladder_score_monster: int
    pro_ladder_score_nilfgaard: int
    pro_ladder_score_northern_kingdom: int
    pro_ladder_score_scoiatael: int
    pro_ladder_score_skellige: int
    pro_ladder_score_syndicate: int
    pro_ladder_games_monster: int
    pro_ladder_games_nilfgaard: int
    pro_ladder_games_northern_kingdom: int
    pro_ladder_games_scoiatael: int
    pro_ladder_games_skellige: int
    pro_ladder_games_syndicate: int


class ProfileDataParagonSchema(BaseModel):
    paragon_level: int
    player_level: int
    current_level_experience: int
    next_level_required_experience: int


class FullProfileDataSchema(BaseModel):
    id: str
    progress_bar: ProfileDataProgressBarSchema
    accomplishments: list[ProfileDataAccomplishmentSchema]
    stats: ProfileDataStatsSchema
    public_profile_hidden: bool
    platform: str
    paragon: ProfileDataParagonSchema


class GwentSitePlayerInfoSchema(BaseModel):
    place: int
    country: str
    nickname: str
    matches: str
    mmr: str


class RanksThresholdSchema(BaseModel):
    rank8: GwentSitePlayerInfoSchema
    rank32: GwentSitePlayerInfoSchema
    rank200: GwentSitePlayerInfoSchema
    rank500: GwentSitePlayerInfoSchema