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
                        }
                    ),
                )

                self.assertDictEqual({"msg": "user created"}, json.loads(response.data))
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_email("troubnique@gmail.com"))

    def test_register_and_login(self):
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
                            "birthday": "16-10-1997",
                        }
                    ),
                )
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
                        }
                    ),
                )

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(
                    {"msg": "Пользователь с таким адресом почты уже существует!"},
                    json.loads(response.data),
                )
