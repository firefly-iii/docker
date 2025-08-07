import unittest
import requests

BASE_URL = "http://localhost:8080/api/v1/accounts"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZGQ4NzhiMDhlYzI3YzFkZTcwYmUyNjI1MDRiZTg1N2M0MTdiMDQ4YzdlZjNjMDA3YmNmZWNmNTM1NGJmNDdlZGNhZDczNDIyOTk0M2U2ZjMiLCJpYXQiOjE3NTQyMTE0NTAuNzE0MzA2LCJuYmYiOjE3NTQyMTE0NTAuNzE0MzEzLCJleHAiOjE3ODU3NDc0NDkuNDAzNDQ4LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.PDVe2nJpSRA8EdKUX2QalQjROp0rOjp94n1jR7xR12mX_bFmJAmqIGgXIIFMghEtMIw6exBedJ6_FlAYs0sDBPXnFSfKuEyNNrKGbwjV1XJktFjZvL1okg5OF2g7_pM6qH5CCjz9p0nHvQ5QnMMRBw-Z38GUhZbzF1jm49VtHk2J0_7nk8ko4C9dpRzkR2LemtivntAW8mgzQNJxVElmVQfOO4UNsiDZ8aDV6V1R0JjK_e29yf73AXz7V8zUngXytSpMOUC7LV2_d65xRThXFKsoUgRaFtthelZK0_PYsUq6HeU47YY1gfRySZQ23-d72t7dw1JCmW_QZ3ccwbLz13C1jeBbzHajRsdNraJoGn1KSSaoJ6yFHR0QBN4NwUeVRS1viKEAAYRwJfcUWWx33HfmfTOkh4yssnf7FoSIPggPt-A2rKYwjUR8OWaDdvBNkydoZTycWO2aAA9FOjbJj-l7_Fq4KbQ9Oj-7UODNbNeHKSOcwaah5xgr7r--54InP3ZHK7CzdweK3UewzDM7NGa7_V63piCqig2i_j9ygQPnsLR_raLah1cRNBGwg5ge-wEBZN2ovIz6xxnZ-d0pBVrv_wqHd3G_5IQbjISubix9mpd-TMRt8I9Jsrd9LSkf0iXitwtAr6AHiBZ-GX3IJDEWiV7gc9aHjrX3JFYl_pE"

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
