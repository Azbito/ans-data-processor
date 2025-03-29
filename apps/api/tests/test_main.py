import pytest
from main import app


def test_read_root():

    response = app.routes[-1].endpoint()
    assert response == {"message": "ping"}


def test_app_routes():

    routes = [route.path for route in app.routes]
    assert "/pdf/ans" in routes
    assert "/pdf/embed_ans_pdf" in routes
    assert "/csv/extract-tables" in routes
    assert "/csv/download-tables" in routes
