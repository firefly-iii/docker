import unittest
import requests

from tests.firefly_credentials import get_firefly_credentials

TOKEN = get_firefly_credentials()["token"]
BASE_URL = get_firefly_credentials()["base_url"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

class TestFireflyAccountsAPI(unittest.TestCase):

    def test_get_accounts_list_success(self):
        params = {
            "limit": 50,
            "page": 1
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        print("Response status:", response.status_code)
        print("Response body:", response.text)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")
        json_data = response.json()

        self.assertIn("data", json_data)
        self.assertIsInstance(json_data["data"], list)

        for account in json_data["data"]:
            self.assertIn("id", account)
            self.assertIn("attributes", account)
            self.assertIn("name", account["attributes"])

    def test_number_of_accounts_not_zero(self):
        """בודק שיש לפחות חשבון אחד"""
        response = requests.get(BASE_URL + "?limit=999", headers=HEADERS)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")
        json_data = response.json()

        self.assertIn("data", json_data)
        account_list = json_data["data"]

        self.assertGreater(len(account_list), 0, f"Expected at least 1 account, but got {len(account_list)}")


if __name__ == "__main__":
    unittest.main()
