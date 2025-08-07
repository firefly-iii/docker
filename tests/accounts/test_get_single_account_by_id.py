import unittest
import requests
import uuid

BASE_URL = "http://localhost:8080/api/v1/accounts"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZGQ4NzhiMDhlYzI3YzFkZTcwYmUyNjI1MDRiZTg1N2M0MTdiMDQ4YzdlZjNjMDA3YmNmZWNmNTM1NGJmNDdlZGNhZDczNDIyOTk0M2U2ZjMiLCJpYXQiOjE3NTQyMTE0NTAuNzE0MzA2LCJuYmYiOjE3NTQyMTE0NTAuNzE0MzEzLCJleHAiOjE3ODU3NDc0NDkuNDAzNDQ4LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.PDVe2nJpSRA8EdKUX2QalQjROp0rOjp94n1jR7xR12mX_bFmJAmqIGgXIIFMghEtMIw6exBedJ6_FlAYs0sDBPXnFSfKuEyNNrKGbwjV1XJktFjZvL1okg5OF2g7_pM6qH5CCjz9p0nHvQ5QnMMRBw-Z38GUhZbzF1jm49VtHk2J0_7nk8ko4C9dpRzkR2LemtivntAW8mgzQNJxVElmVQfOO4UNsiDZ8aDV6V1R0JjK_e29yf73AXz7V8zUngXytSpMOUC7LV2_d65xRThXFKsoUgRaFtthelZK0_PYsUq6HeU47YY1gfRySZQ23-d72t7dw1JCmW_QZ3ccwbLz13C1jeBbzHajRsdNraJoGn1KSSaoJ6yFHR0QBN4NwUeVRS1viKEAAYRwJfcUWWx33HfmfTOkh4yssnf7FoSIPggPt-A2rKYwjUR8OWaDdvBNkydoZTycWO2aAA9FOjbJj-l7_Fq4KbQ9Oj-7UODNbNeHKSOcwaah5xgr7r--54InP3ZHK7CzdweK3UewzDM7NGa7_V63piCqig2i_j9ygQPnsLR_raLah1cRNBGwg5ge-wEBZN2ovIz6xxnZ-d0pBVrv_wqHd3G_5IQbjISubix9mpd-TMRt8I9Jsrd9LSkf0iXitwtAr6AHiBZ-GX3IJDEWiV7gc9aHjrX3JFYl_pE"

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
