from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LevelType(str, Enum):
    RIVER_LEVEL = "river_level"
    FLOW = "flow"


class LevelUnit(str, Enum):
    M = "m"
    M3_S = "m3/s"


class BaseGaugeReading(BaseModel):
    river_section: str
    datetime: datetime
    level: str
    level_type: LevelType
    level_unit: LevelUnit


class FlowGaugeReading(BaseGaugeReading):
    level_type: LevelType = LevelType.FLOW
    level_unit: LevelUnit = LevelUnit.M3_S


class LevelGaugeReading(BaseGaugeReading):
    level_type: LevelType = LevelType.RIVER_LEVEL
    level_unit: LevelUnit = LevelUnit.M
