from pathlib import Path

import pandas
from river_connectors.cehq import create_cehq_gauge_readings, fetch_cehq_station_data

TESTS_RESOURCES_FOLDER = Path(__file__).parent / "resources"


def test_fetch_cehq_station_data():
    data = fetch_cehq_station_data("040204")
    assert data is not None
    assert [column.strip() for column in data.columns.tolist()] == ["Date", "Heure", "Débit"]


def test_create_cehq_gauge_readings():
    data = pandas.read_csv(TESTS_RESOURCES_FOLDER / "cehq_040204.csv")
    readings = create_cehq_gauge_readings("040204", data)
    assert readings is not None
    assert len(readings) == len(data)
