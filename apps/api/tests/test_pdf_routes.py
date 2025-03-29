import pytest
from routes.pdf import router


def test_router_has_correct_routes():

    route_paths = [route.path for route in router.routes]
    assert "/pdf/ans" in route_paths
    assert "/pdf/embed_ans_pdf" in route_paths
