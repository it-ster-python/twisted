# import unittest
# from data import models
# from utils import tools
#
#
# class TestUserModel(unittest.TestCase):
#     def setUp(self):
#         self.model = models.User
#         self.test_data = {"login": "admin", "hash_pass": "*"}
#
#     def test_create_model_1(self):
#         user = self.model()
#         # self.assertRaises(AssertionError, user.id)
#         user.login = self.test_data["login"]
#         user.hash_pass = self.test_data["hash_pass"]
#         user.save()
#         self.assertIsInstance(user.id, int)
#
#     def test_create_model_2(self):
#         user = self.model(**self.test_data)
#         user.save()
#
#     def tearDown(self):
#         self.model.truncate_table(restart_identity=True, cascade=True)
#
#
# class TestHashPassword(unittest.TestCase):
#     def setUp(self):
#         self.test_data = {"password": "admin", "salt": "dajlghlkasdflasdkkfh"}
#         self.test_data_error = {
#             "password": "adminadmin",
#             "salt": "dajlghlkasdflasdkkfdsgfh",
#         }
#
#     def test_1_hash_pass(self):
#         pass_hash = tools.hash256(
#             tools.str_to_sotr_list(
#                 self.test_data.get("password"), self.test_data.get("salt")
#             )
#         )
#         error_data = tools.str_to_sotr_list(
#             self.test_data_error.get("salt"), self.test_data_error.get("password")
#         )
#         self.assertEqual(
#             pass_hash,
#             tools.hash256(
#                 tools.str_to_sotr_list(
#                     self.test_data.get("password"), self.test_data.get("salt")
#                 )
#             ),
#         )
#         self.assertNotEqual(pass_hash, tools.hash256(error_data))
#
#
# class TestSaltCreate(unittest.TestCase):
#     def setUp(self):
#         self.user = models.User(login="admin", hash_pass="*")
#         self.user.save()
#         self.model = models.Salt
#
#     def test_create_model(self):
#         salt = self.model()
#         self.assertIsNotNone(salt.salt)
#         self.assertEqual(salt.salt, salt.value)
#
#     def test_save_salt(self):
#         record = self.model(user_id=self.user.id)
#         record.save()
#         record_test = self.model.get(id=record.id)
#         self.assertEqual(record.id, record_test.id)
#         self.assertEqual(record.value, record_test.salt)
#         self.assertEqual(record.salt, record_test.salt)
#
#     def tearDown(self):
#         models.User.truncate_table(restart_identity=True, cascade=True)
#         self.model.truncate_table(restart_identity=True, cascade=True)
#
#
# class TestUserLogin(unittest.TestCase):
#     def setUp(self):
#         self.test_data = {"login": "admin", "password": "admin"}
#         self.test_error_data = {"login": "admin", "password": "1234555"}
#         self.test_pass_data = {"login": "User", "password": "12345678"}
#         user = models.User()
#         salt = models.Salt()
#         user.login = self.test_data.get("login")
#         user.hash_pass = tools.hash256(
#             tools.str_to_sotr_list(self.test_data.get("password"), salt.value)
#         )
#         user.save()
#         salt.user = user
#         salt.save()
#
#     def test_login_pass(self):
#         user = models.User.get(login=self.test_data.get("login"))
#         salt = user.salt[0].value
#         hash_pass = tools.hash256(
#             tools.str_to_sotr_list(self.test_data.get("password"), salt)
#         )
#         self.assertEqual(user.hash_pass, hash_pass)
#
#     def test_error_login(self):
#         user = models.User.get(login=self.test_error_data.get("login"))
#         salt = models.Salt.get(user=user)
#         hash_pass = tools.hash256(
#             tools.str_to_sotr_list(self.test_error_data.get("password"), salt.value)
#         )
#         self.assertNotEqual(user.hash_pass, hash_pass)
#
#     def test_is_login(self):
#         user = models.User.get(login=self.test_data.get("login"))
#         self.assertTrue(user.check_password(self.test_data.get("password")))
#
#     def test_attr_password(self):
#         user = models.User()
#         user.password = self.test_pass_data["password"]
#         user.login = self.test_pass_data["login"]
#         user.save()
#
#         test_user = models.User.get(login=self.test_pass_data["login"])
#         hash_data = tools.hash256(
#             tools.str_to_sotr_list(
#                 self.test_pass_data["password"],
#                 test_user.salt[0].value
#             )
#         )
#         self.assertEqual(test_user.hash_pass, hash_data)
#
#     def tearDown(self):
#         models.User.truncate_table(restart_identity=True, cascade=True)
#         models.Salt.truncate_table(restart_identity=True, cascade=True)
#
#
# if __name__ == "__main__":
#     unittest.main()
