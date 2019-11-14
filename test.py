import unittest
from data import models


class TestUserModel(unittest.TestCase):

    def setUp(self):
        self.model = models.User
        self.test_data = {
            "login": "admin",
            "hash_pass": "*"
        }

    def test_create_model_1(self):
        user = self.model()
        self.assertRaises(AssertionError, user.id)
        user.login = self.test_data["login"]
        user.hash_pass = self.test_data["hash_pass"]
        user.save()
        self.assertIsInstance(user.id, int)

    def test_create_model_2(self):
        user = self.model(**self.test_data)
        user.save()

    def tearDown(self):
        self.model.truncate_table(
            restart_identity=True, cascade=True
        )


if __name__ == '__main__':
    unittest.main()
