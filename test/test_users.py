from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current

def test_return_user(test_user):
  response =  client.get("/user")
  assert response.status_code == status.HTTP_200_OK
  assert response.json()['username'] == 'graciasdevtest'


def test_update_password_success(test_user):
  response = client.put("/user/password", json={"password": "test1234", "new_password": "newpassword"})
  assert response.status_code == status.HTTP_204_NO_CONTENT


def test_update_password_invalid(test_user):
  response = client.put("/user/password", json={"password": "wrong_password", "new_password": "newpassword"})
  assert response.status_code == status.HTTP_401_UNAUTHORIZED
  assert response.json() == {'detail': 'Error on password change'}


def test_update_phoe_number_success(test_user):
  response = client.put('/user/phonenumber/222222222222')
  assert response.status_code == status.HTTP_204_NO_CONTENT
