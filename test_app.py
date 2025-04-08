import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
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
    assert response.get_json()['message'] == "User created successfully"

