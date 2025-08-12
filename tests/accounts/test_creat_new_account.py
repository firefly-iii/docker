import unittest
import requests
import uuid

from tests.firefly_credentials import get_firefly_credentials


TOKEN = get_firefly_credentials()["token"]
BASE_URL = get_firefly_credentials()["base_url"]
ACCOUNTS_URL = BASE_URL + "/api/v1/accounts"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

class TestFireflyCreateAccount(unittest.TestCase):

    def get_account_count(self):
        response = requests.get(ACCOUNTS_URL + "?limit=999", headers=HEADERS)
        self.assertEqual(response.status_code, 200, "Failed to fetch accounts list")
        data = response.json()
        return len(data.get("data", []))



    def test_create_account_success(self):
        initial_count = self.get_account_count()

        unique_name = f"My testing account {uuid.uuid4()}"  # שם ייחודי בכל הרצה
        payload = {
            "name": unique_name,
            "type": "asset",
            "account_role": "defaultAsset",
            "currency_id": "1"
        }

        response = requests.post(ACCOUNTS_URL, headers=HEADERS, json=payload)

        print("Response status:", response.status_code)
        print("Response body:", response.text)

        self.assertEqual(response.status_code, 200, f"Expected 200 but got {response.status_code}")
        data = response.json()
        self.assertIn("data", data)
        self.assertEqual(data["data"]["attributes"]["name"], unique_name)

        final_count = self.get_account_count()
        self.assertEqual(final_count, initial_count + 1, f"Expected {initial_count + 1} accounts but got {final_count}")

    def test_create_account_missing_required_field(self):
        incomplete_payload = {
            "type": "asset"
        }

        response = requests.post(ACCOUNTS_URL, headers=HEADERS, json=incomplete_payload)
        self.assertEqual(response.status_code, 422)
        json_data = response.json()
        self.assertIn("message", json_data)
        self.assertIn("errors", json_data)
        self.assertIn("name", json_data["errors"])

    def test_duplicate_account_name(self):
        unique_name = f"Duplicate Account {uuid.uuid4()}"
        payload = {
            "name": unique_name,
            "type": "asset",
            "account_role": "defaultAsset",
            "currency_id": "1"
        }

        first = requests.post(ACCOUNTS_URL, headers=HEADERS, json=payload)
        second = requests.post(ACCOUNTS_URL, headers=HEADERS, json=payload)

        # שני הבקשות יהיו עם אותו שם – השנייה אמורה להיכשל
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 422)

if __name__ == "__main__":
    unittest.main()

