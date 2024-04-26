from .common import client


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


first_user_data = {
    "name": "Gonza",
    "lastname": "Sabatino",
    "description": "I like having fun!",
    "date_of_birth": "03-03-2000",
    "photo": "base64-photo",
    "email": "email@email.com",
    "id": "ak345sidsdfo12wm192"
}


def test_create_user():
    response = client.post("/users/", json=first_user_data)
    assert response.status_code == 200
    assert response.json() == first_user_data['id']


def test_create_then_get_user():
    response = client.get(f"/users/{first_user_data['id']}")
    print(response.json())
    assert response.status_code == 200
    assert response.json()['name'] == first_user_data['name']


def test_change_user():
    first_user_data['name'] = 'Mateito'
    response = client.put("/users/", json=first_user_data)
    assert response.status_code == 200
    assert response.json()['name'] == 'Mateito'
