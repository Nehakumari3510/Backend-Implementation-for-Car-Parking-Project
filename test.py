import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # use in-memory DB for testing
    with app.app_context():
        db.create_all()  # create tables in the test DB
    with app.test_client() as client:
        yield client

def test_parking_lot_empty(client):
    response = client.get('/parking_lot')
    assert response.status_code == 200
    assert isinstance(response.get_json(), dict)
