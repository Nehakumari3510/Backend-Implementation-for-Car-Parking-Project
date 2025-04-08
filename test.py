import pytest
from backend import app, db 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"  # test in-memory DB
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def test_create_user(client):
    user_data = {
        "user_name": "Test User",
        "user_email": "test@example.com",
        "user_password": "secret",
        "user_phone_no": "1234567890",
        "user_address": "Test Address"
    }
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert "user_id" in json_data
