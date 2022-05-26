import unittest
import json

import app_sql

BASE_URL = "http://127.0.0.1:5000"

class MarketplaceAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app_sql.app.test_client()
        self.app.testing = True

    def test_get_user(self):
        expected_output = {"id": "3b867c2c-98f8-425e-a992-22e6e54f958a", "name": "First User", "email": "first@user.com", "register_date": "2022-05-25 20:13"}
        response = self.app.get(BASE_URL + "/get_user/3b867c2c-98f8-425e-a992-22e6e54f958a")
        actual_output = json.loads(response.get_data())
        self.assertEqual(expected_output, actual_output)
        self.assertEqual(response.status_code, 200)

    # TODO: add test for all operations... list_users, delete_user, add_user, etc

if __name__ == '__main__':
    unittest.main()