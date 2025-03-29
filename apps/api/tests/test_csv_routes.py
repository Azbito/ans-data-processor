import pytest
from routes.csv import router


def test_router_has_correct_routes():

    route_paths = [route.path for route in router.routes]
    assert "/csv/extract-tables" in route_paths
    assert "/csv/download-tables" in route_paths
