from datetime import datetime
from io import StringIO
from zoneinfo import ZoneInfo

import pandas
import requests
from river_core.domain.readings import FlowGaugeReading
from river_core.errors import RiverConnectorError

CEHQ_BASE_URL = "https://www.cehq.gouv.qc.ca/suivihydro/fichier_donnees.asp?NoStation="

CEHQ_DATE = "Date"
CEHQ_TIME = "Heure"
CEHQ_LEVEL = "Débit"
CEHQ_COLUMNS = frozenset([CEHQ_DATE, CEHQ_TIME, CEHQ_LEVEL])

gauge_info = {"040204": "Rivière Rouge"}


def format_date_time(date: str, time: str) -> datetime:
    """Format a date and time string into a datetime object.

    Args:
        date: The date string.
        time: The time string.

    Returns:
        The formatted datetime object.
    """
    clean_date = date.strip()
    clean_time = time.strip()
    formatted_date = datetime.strptime(f"{clean_date} {clean_time}", "%Y-%m-%d %H:%M")
    formatted_date = formatted_date.replace(tzinfo=ZoneInfo("EST"))
    return formatted_date


def fetch_cehq_station_data(station_id: str) -> pandas.DataFrame:
    """Fetch data from the CEHQ API for a specific station.

    Args:
        station_id: The ID of the station to fetch data for.

    Returns:
        pandas.DataFrame: The data for the station.
    """
    station_url = f"{CEHQ_BASE_URL}{station_id}"
    data = requests.get(station_url).text
    df = pandas.read_csv(StringIO(data), sep="\t", lineterminator="\n")
    df[CEHQ_LEVEL] = df[CEHQ_LEVEL].map(lambda x: x.rstrip("*"))
    df.columns = df.columns.str.strip()
    return df


def create_cehq_gauge_readings(station_id: str, df: pandas.DataFrame) -> list[FlowGaugeReading]:
    """Create gauge readings from a DataFrame of CEHQ data.

    Args:
        station_id: The id of the river gauge.
        df: The DataFrame of CEHQ data.

    Returns:
        list[FlowGaugeReading]: The list of gauge readings.
    """
    required_columns = list(CEHQ_COLUMNS)
    if not all(str(col).strip() in df.columns for col in required_columns):
        raise RiverConnectorError(
            f"Error while creating CEHQ gauge readings for {station_id}: Missing required columns"
        )

    gauge_name = gauge_info.get(station_id, "Unknown")

    readings_list = [
        FlowGaugeReading(
            gauge_id=station_id,
            gauge_name=gauge_name,
            datetime=format_date_time(date=date, time=time),
            level=flow,
        )
        for date, time, flow in zip(df[CEHQ_DATE], df[CEHQ_TIME], df[CEHQ_LEVEL])
    ]
    return readings_list
