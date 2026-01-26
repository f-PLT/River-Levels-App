from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class LevelType(str, Enum):
    """Level type."""

    RIVER_LEVEL = "river_level"
    FLOW = "flow"


class LevelUnit(str, Enum):
    """Level unit."""

    M = "m"
    M3_S = "m3/s"


class BaseGaugeReading(BaseModel):
    """Base gauge reading.

    Attributes:
        gauge_id (str): The id of the gauge.
        gauge_name (str): The name of the gauge.
        datetime (datetime): The datetime of the reading.
        level (str): The level of the reading.
        level_type (LevelType): The type of the level.
        level_unit (LevelUnit): The unit of the level.
    """

    gauge_id: str
    gauge_name: str
    datetime: datetime
    level: str
    level_type: LevelType
    level_unit: LevelUnit


class FlowGaugeReading(BaseGaugeReading):
    """Flow gauge reading.

    Attributes:
        level_type (LevelType): The type of the level.
        level_unit (LevelUnit): The unit of the level.
    """

    level_type: LevelType = LevelType.FLOW
    level_unit: LevelUnit = LevelUnit.M3_S


class LevelGaugeReading(BaseGaugeReading):
    """Level gauge reading.

    Attributes:
        level_type (LevelType): The type of the level.
        level_unit (LevelUnit): The unit of the level.
    """

    level_type: LevelType = LevelType.RIVER_LEVEL
    level_unit: LevelUnit = LevelUnit.M
