from tellr.schemas.user import UserSchema
from tellr.models.user import UserModel
from tellr.tests.base_test import BaseTest

user_schema = UserSchema()


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = user_schema.load(
                {
                    "email": "egorque@gmail.com",
                    "password": "12345",
                    "first_name": "Егор",
                    "sex": True,
                }
            )

            self.assertIsNone(UserModel.find_by_email("egorque@gmail.com"))
            self.assertIsNone(UserModel.find_by_id(1))

            user.save_to_db()

            self.assertIsNotNone(UserModel.find_by_email("egorque@gmail.com"))
            self.assertIsNotNone(UserModel.find_by_id(1))

            user_profile = user_schema.dump(
                UserModel.find_by_email("egorque@gmail.com")
            )

            self.assertEqual(user_profile["age"], 21)
            self.assertEqual(user_profile["first_name"], "Егор")
            self.assertTrue(user_profile["sex"])
            user.delete_from_db()

            self.assertIsNone(UserModel.find_by_email("egorque@gmail.com"))
            self.assertIsNone(UserModel.find_by_id(1))
