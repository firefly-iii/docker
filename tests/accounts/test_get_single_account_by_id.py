import unittest
import requests
import uuid

from tests.firefly_credentials import get_firefly_credentials


TOKEN = get_firefly_credentials()["token"]
BASE_URL = get_firefly_credentials()["base_url"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.api+json",
    "X-Trace-Id": str(uuid.uuid4())
}


class TestGetSingleAccount(unittest.TestCase):

    def test_get_existing_account(self):
        account_id = "2"  # ודא שהחשבון הזה קיים
        response = requests.get(f"{BASE_URL}/{account_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 200, msg=response.text)
        data = response.json()
        self.assertIn("data", data)
        self.assertEqual(data["data"]["id"], account_id)
        self.assertEqual(data["data"]["type"], "accounts")

    def test_get_nonexistent_account(self):
        account_id = "999999"  # ID שלא קיים
        response = requests.get(f"{BASE_URL}/{account_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 404, msg=response.text)
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Resource not found")

    def test_get_account_unauthenticated(self):
        account_id = "2"
        headers_without_token = {
            "Accept": "application/vnd.api+json",
            "X-Trace-Id": str(uuid.uuid4())
        }
        response = requests.get(f"{BASE_URL}/{account_id}", headers=headers_without_token)
        self.assertEqual(response.status_code, 401, msg=response.text)
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Unauthenticated.")

    def test_get_account_bad_request(self):
        invalid_id = "invalid-id"
        response = requests.get(f"{BASE_URL}/{invalid_id}", headers=HEADERS)
        self.assertIn(response.status_code, [400, 404], msg=response.text)
        data = response.json()
        self.assertIn("message", data)


if __name__ == "__main__":
    unittest.main()
