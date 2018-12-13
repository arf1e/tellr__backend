from unittest import TestCase

from tellr.models.user import UserModel


class UserTest(TestCase):
    def test_create_user(self):
        user = UserModel("egorque", "12345", "Егор", True)

        self.assertEqual(
            user.username, "egorque", "Юзернейм пользователя не совпадает с ожидаемым"
        )
        self.assertEqual(
            user.first_name, "Егор", "Имя пользователя не совпадает с ожидаемым"
        )
        self.assertEqual(user.sex, True)

    def test_user_json(self):
        pass
