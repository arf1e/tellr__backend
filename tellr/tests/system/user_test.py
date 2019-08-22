from tellr.models.user import UserModel
from tellr.tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:  # new app instance
            with self.app_context():  # initializes db
                response = client.post(
                    "/register",
                    headers={"Content-type": "application/json"},
                    data=json.dumps(
                        {
                            "email": "troubnique@gmail.com",
                            "password": "sudobangbang",
                            "first_name": "Слава",
                            "sex": True,
                            "city": "Санкт-Петербург",
                            "city_id": "ChIJ7WVKx4w3lkYR_46Eqz9nx20",
                        }
                    ),
                )
                print(response)
                # user logged in
                self.assertIn("access_token", json.loads(response.data).keys())
                self.assertIn("refresh_token", json.loads(response.data).keys())
                # correct code
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_email("troubnique@gmail.com"))

    def test_register_logout_and_login(self):
        with self.app() as client:  # new app instance
            with self.app_context():  # initializes db
                response = client.post(
                    "/register",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "email": "troubnique@gmail.com",
                            "password": "sudobangbang",
                            "first_name": "Слава",
                            "sex": True,
                            "birthday": "16-10-1997",
                            "city": "Санкт-Петербург",
                            "city_id": "ChIJ7WVKx4w3lkYR_46Eqz9nx20",
                        }
                    ),
                )
                token = json.loads(response.data)["access_token"]
                logout_response = client.post(
                    "/logout",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}",
                    },
                )
                # User logged out
                self.assertEqual(logout_response.status_code, 200)
                login_response = client.post(
                    "/login",
                    data=json.dumps(
                        {"email": "troubnique@gmail.com", "password": "sudobangbang"}
                    ),
                    headers={"Content-Type": "application/json"},
                )
                self.assertIn("access_token", json.loads(login_response.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:  # new app instance
            with self.app_context():  # initializes db
                client.post(
                    "/register",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "email": "troubnique@gmail.com",
                            "password": "sudobangbang",
                            "first_name": "Слава",
                            "sex": True,
                            "city": "Санкт-Петербург",
                            "city_id": "ChIJ7WVKx4w3lkYR_46Eqz9nx20",
                        }
                    ),
                )
                response = client.post(
                    "/register",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "email": "troubnique@gmail.com",
                            "password": "sudobangbang",
                            "first_name": "Слава",
                            "sex": True,
                            "city": "Санкт-Петербург",
                            "city_id": "ChIJ7WVKx4w3lkYR_46Eqz9nx20",
                        }
                    ),
                )

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    {"msg": "Пользователь с таким адресом почты уже существует!"},
                    json.loads(response.data),
                )
