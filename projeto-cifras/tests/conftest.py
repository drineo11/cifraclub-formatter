import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.index import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


@pytest.fixture
def valid_cifra_url():
    return "https://www.cifraclub.com.br/artista/titulo/"


@pytest.fixture
def sample_lines():
    return [
        [{"text": "[Intro]", "bold": False}],
        [
            {"text": "C", "bold": True},
            {"text": " G", "bold": False},
            {"text": " Am", "bold": True},
            {"text": " F", "bold": False},
        ],
        [{"text": "Esta é a letra", "bold": False}],
        [{"text": "[Verso]", "bold": False}],
        [{"text": "D", "bold": True}, {"text": " m", "bold": False}],
        [{"text": "Outra linha", "bold": False}],
    ]
