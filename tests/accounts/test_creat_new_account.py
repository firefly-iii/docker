import unittest
import requests
import uuid

BASE_URL = "http://localhost:8080/api/v1/accounts"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZGQ4NzhiMDhlYzI3YzFkZTcwYmUyNjI1MDRiZTg1N2M0MTdiMDQ4YzdlZjNjMDA3YmNmZWNmNTM1NGJmNDdlZGNhZDczNDIyOTk0M2U2ZjMiLCJpYXQiOjE3NTQyMTE0NTAuNzE0MzA2LCJuYmYiOjE3NTQyMTE0NTAuNzE0MzEzLCJleHAiOjE3ODU3NDc0NDkuNDAzNDQ4LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.PDVe2nJpSRA8EdKUX2QalQjROp0rOjp94n1jR7xR12mX_bFmJAmqIGgXIIFMghEtMIw6exBedJ6_FlAYs0sDBPXnFSfKuEyNNrKGbwjV1XJktFjZvL1okg5OF2g7_pM6qH5CCjz9p0nHvQ5QnMMRBw-Z38GUhZbzF1jm49VtHk2J0_7nk8ko4C9dpRzkR2LemtivntAW8mgzQNJxVElmVQfOO4UNsiDZ8aDV6V1R0JjK_e29yf73AXz7V8zUngXytSpMOUC7LV2_d65xRThXFKsoUgRaFtthelZK0_PYsUq6HeU47YY1gfRySZQ23-d72t7dw1JCmW_QZ3ccwbLz13C1jeBbzHajRsdNraJoGn1KSSaoJ6yFHR0QBN4NwUeVRS1viKEAAYRwJfcUWWx33HfmfTOkh4yssnf7FoSIPggPt-A2rKYwjUR8OWaDdvBNkydoZTycWO2aAA9FOjbJj-l7_Fq4KbQ9Oj-7UODNbNeHKSOcwaah5xgr7r--54InP3ZHK7CzdweK3UewzDM7NGa7_V63piCqig2i_j9ygQPnsLR_raLah1cRNBGwg5ge-wEBZN2ovIz6xxnZ-d0pBVrv_wqHd3G_5IQbjISubix9mpd-TMRt8I9Jsrd9LSkf0iXitwtAr6AHiBZ-GX3IJDEWiV7gc9aHjrX3JFYl_pE"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

class TestFireflyCreateAccount(unittest.TestCase):

    def get_account_count(self):
        response = requests.get(BASE_URL + "?limit=999", headers=HEADERS)
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

        response = requests.post(BASE_URL, headers=HEADERS, json=payload)

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

        response = requests.post(BASE_URL, headers=HEADERS, json=incomplete_payload)
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

        first = requests.post(BASE_URL, headers=HEADERS, json=payload)
        second = requests.post(BASE_URL, headers=HEADERS, json=payload)

        # שני הבקשות יהיו עם אותו שם – השנייה אמורה להיכשל
        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 422)

if __name__ == "__main__":
    unittest.main()
