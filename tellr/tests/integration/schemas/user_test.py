from tellr.schemas.user import UserSchema
from tellr.models.user import UserModel
from tellr.tests.base_test import BaseTest

user_schema = UserSchema()


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = user_schema.load(
                {
                    "username": "egorque",
                    "password": "12345",
                    "first_name": "Егор",
                    "sex": True,
                }
            )

            self.assertIsNone(UserModel.find_by_username("egorque"))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_username("egorque"))
            self.assertIsNotNone(UserModel.find_by_id(1))

            user_profile = user_schema.dump(UserModel.find_by_username("egorque"))

            self.assertEqual(user_profile["age"], 21)
            self.assertEqual(user_profile["first_name"], "Егор")
            self.assertTrue(user_profile["sex"])
            self.assertEqual(
                user_profile["avatar"], "/static/images/avatars/flower.png"
            )

            user.delete_from_db()

            self.assertIsNone(UserModel.find_by_username("egorque"))
            self.assertIsNone(UserModel.find_by_id(1))
