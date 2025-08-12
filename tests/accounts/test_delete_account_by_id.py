import unittest
import uuid
import requests
from tests.firefly_credentials import get_firefly_credentials

TOKEN = get_firefly_credentials()["token"]
BASE_URL = get_firefly_credentials()["base_url"]

DELETE_URL = f"{BASE_URL}/api/v1/accounts/{{id}}"
CREATE_ACCOUNTS_URL = BASE_URL + "/api/v1/accounts"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-Trace-Id": str(uuid.uuid4())
}

class TestDeleteAccountAPI(unittest.TestCase):
    def create_temp_account(self):
        payload = {
            "name": f"Temp Account {uuid.uuid4()}",
            "type": "asset",
            "account_role": "defaultAsset",
            "currency_id": "1"
        }
        response = requests.post(CREATE_ACCOUNTS_URL, headers=HEADERS, json=payload)
        self.assertEqual(response.status_code, 200, "Failed to create temporary account")
        return response.json()["data"]["id"]

    def test_delete_existing_account_success(self):
        account_id = self.create_temp_account()
        delete_url = DELETE_URL.format(id=account_id)
        response = requests.delete(delete_url, headers=HEADERS)
        self.assertEqual(response.status_code, 204)

    def test_delete_nonexistent_account(self):
        fake_id = "999999999"
        delete_url = DELETE_URL.format(id=fake_id)
        response = requests.delete(delete_url, headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Resource not found", response.text)

    def test_delete_account_missing_authentication(self):
        account_id = self.create_temp_account()
        delete_url = DELETE_URL.format(id=account_id)
        headers = HEADERS.copy()
        headers.pop("Authorization")  # בלי טוקן
        response = requests.delete(delete_url, headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthenticated", response.text)

    def test_delete_account_invalid_format(self):
        # מזהה לא תקין – נצפה ל־404 (ולא 400)
        bad_id = "!!invalid_id!!"
        delete_url = DELETE_URL.format(id=bad_id)
        response = requests.delete(delete_url, headers=HEADERS)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Resource not found", response.text)

if __name__ == "__main__":
    unittest.main()
