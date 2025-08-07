import unittest
import uuid
import requests

BASE_URL = "http://localhost:8080/api/v1/accounts"
DELETE_URL = f"{BASE_URL}/{{id}}"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZGQ4NzhiMDhlYzI3YzFkZTcwYmUyNjI1MDRiZTg1N2M0MTdiMDQ4YzdlZjNjMDA3YmNmZWNmNTM1NGJmNDdlZGNhZDczNDIyOTk0M2U2ZjMiLCJpYXQiOjE3NTQyMTE0NTAuNzE0MzA2LCJuYmYiOjE3NTQyMTE0NTAuNzE0MzEzLCJleHAiOjE3ODU3NDc0NDkuNDAzNDQ4LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.PDVe2nJpSRA8EdKUX2QalQjROp0rOjp94n1jR7xR12mX_bFmJAmqIGgXIIFMghEtMIw6exBedJ6_FlAYs0sDBPXnFSfKuEyNNrKGbwjV1XJktFjZvL1okg5OF2g7_pM6qH5CCjz9p0nHvQ5QnMMRBw-Z38GUhZbzF1jm49VtHk2J0_7nk8ko4C9dpRzkR2LemtivntAW8mgzQNJxVElmVQfOO4UNsiDZ8aDV6V1R0JjK_e29yf73AXz7V8zUngXytSpMOUC7LV2_d65xRThXFKsoUgRaFtthelZK0_PYsUq6HeU47YY1gfRySZQ23-d72t7dw1JCmW_QZ3ccwbLz13C1jeBbzHajRsdNraJoGn1KSSaoJ6yFHR0QBN4NwUeVRS1viKEAAYRwJfcUWWx33HfmfTOkh4yssnf7FoSIPggPt-A2rKYwjUR8OWaDdvBNkydoZTycWO2aAA9FOjbJj-l7_Fq4KbQ9Oj-7UODNbNeHKSOcwaah5xgr7r--54InP3ZHK7CzdweK3UewzDM7NGa7_V63piCqig2i_j9ygQPnsLR_raLah1cRNBGwg5ge-wEBZN2ovIz6xxnZ-d0pBVrv_wqHd3G_5IQbjISubix9mpd-TMRt8I9Jsrd9LSkf0iXitwtAr6AHiBZ-GX3IJDEWiV7gc9aHjrX3JFYl_pE"
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
        response = requests.post(BASE_URL, headers=HEADERS, json=payload)
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
