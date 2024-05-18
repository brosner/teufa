import pytest

from teufa.app import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app
