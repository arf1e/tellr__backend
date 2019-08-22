from unittest import TestCase
from tellr.schemas.user import UserSchema
from tellr.models.user import UserModel

user_schema = UserSchema()


class UserTest(TestCase):
    def test_create_user(self):
        user = user_schema.load(
            {
                "email": "egorque@gmail.com",
                "password": "12345",
                "first_name": "Егор",
                "sex": True,
                "city": "Санкт-Петербург",
                "city_id": "ChIJ7WVKx4w3lkYR_46Eqz9nx20",
            }
        )
        self.assertEqual(
            user.email,
            "egorque@gmail.com",
            "Юзернейм пользователя не совпадает с ожидаемым",
        )
        self.assertEqual(
            user.first_name, "Егор", "Имя пользователя не совпадает с ожидаемым"
        )
        self.assertEqual(user.sex, True)
