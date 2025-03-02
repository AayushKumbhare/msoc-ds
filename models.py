from sqlmodel import Field, SQLModel, Column, JSON
from typing import Optional, List
from datetime import datetime

class Athlete(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    gender: Optional[str] = None
    jersey: str
    nickname: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    date_of_birth: Optional[datetime] = None
    velocity_max: Optional[float] = None
    acceleration_max: Optional[float] = None
    heart_rate_max: Optional[int] = None
    player_load_max: Optional[float] = None
    image: Optional[str] = None
    icon: Optional[str] = None
    stroke_colour: Optional[str] = None
    fill_colour: Optional[str] = None
    trail_colour_start: Optional[str] = None
    trail_colour_end: Optional[str] = None
    is_synced: Optional[int] = None
    is_deleted: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    date_of_birth_date: Optional[str] = None
    is_demo: Optional[bool] = None
    current_team_id: Optional[str] = None
    max_player_load_per_minute: Optional[float] = None
    position: Optional[str] = None
    position_id: Optional[str] = None
    position_name: Optional[str] = None


class Activity(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: str = Field(primary_key=True)
    name: str
    start_time: int
    end_time: int
    modified_at: datetime
    game_id: str
    owner_id: str
    athlete_count: int
    period_count: int

    # Relationships
    # owner: Optional["Owner"] = Field(default=None)
    periods: list["Period"] = Field(sa_column=Column(JSON))
    # tags: List[str] = []
    # tag_list: List["Tag"] = []

class Owner(SQLModel, table=True):
    __table_args__ = {"extend_existing": True, "if_not_exists": True}
    id: str = Field(primary_key=True)
    customer_id: int
    name: str
    email: str
    is_synced: int
    is_deleted: int
    created_at: datetime
    modified_at: datetime
    default: int
    full_name: str

class Period(SQLModel, table=True):
    __table_args__ = {"extend_existing": True, "if_not_exists": True}
    id: str = Field(primary_key=True)
    activity_id: str = Field(foreign_key="activity.id")
    period_depth_id: str
    name: str
    start_time: float
    start_centiseconds: int
    end_time: float
    end_centiseconds: int
    lft: int
    rgt: int
    is_synced: int
    is_deleted: int
    is_injected: int
    created_at: datetime
    modified_at: datetime
    user_id: Optional[str]

# class Tag(SQLModel, table=True):
#     __table_args__ = {"extend_existing": True, "if_not_exists": True}
#     id: str = Field(primary_key=True)
#     tag_type_id: str
#     name: str
#     tag_type_name: str
#     tag_name: str
