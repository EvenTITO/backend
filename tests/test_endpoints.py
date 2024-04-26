from .common import client


first_user_data = {
  "id": "aasjdfvhasdvnlaksdj",
  "name": "Lio",
  "surname": "Messi",
  "photo": "base64-photo",
  "email": "email@email.com"
}


def test_create_user():
    response = client.post("/users/", json=first_user_data)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data['id'] == first_user_data['id']
    assert response_data['name'] == first_user_data['name']
    assert response_data['surname'] == first_user_data['surname']
    assert response_data['email'] == first_user_data['email']
    assert response_data['photo'] == first_user_data['photo']


def test_get_user():
    response = client.get(f"/users/{first_user_data['id']}")
    assert response.status_code == 200
    assert response.json()['name'] == first_user_data['name']


def test_create_again_fails():
    response = client.post("/users/", json=first_user_data)
    assert response.status_code == 400


def test_different_id_same_mail_fails():
    other_user = first_user_data.copy()
    other_user["id"] = 'other_id'
    response = client.post("/users/", json=other_user)
    assert response.status_code == 400
