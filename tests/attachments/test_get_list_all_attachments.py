import unittest
import requests
import uuid

BASE_URL = "http://localhost:8080/api/v1/attachments"
TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZGQ4NzhiMDhlYzI3YzFkZTcwYmUyNjI1MDRiZTg1N2M0MTdiMDQ4YzdlZjNjMDA3YmNmZWNmNTM1NGJmNDdlZGNhZDczNDIyOTk0M2U2ZjMiLCJpYXQiOjE3NTQyMTE0NTAuNzE0MzA2LCJuYmYiOjE3NTQyMTE0NTAuNzE0MzEzLCJleHAiOjE3ODU3NDc0NDkuNDAzNDQ4LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.PDVe2nJpSRA8EdKUX2QalQjROp0rOjp94n1jR7xR12mX_bFmJAmqIGgXIIFMghEtMIw6exBedJ6_FlAYs0sDBPXnFSfKuEyNNrKGbwjV1XJktFjZvL1okg5OF2g7_pM6qH5CCjz9p0nHvQ5QnMMRBw-Z38GUhZbzF1jm49VtHk2J0_7nk8ko4C9dpRzkR2LemtivntAW8mgzQNJxVElmVQfOO4UNsiDZ8aDV6V1R0JjK_e29yf73AXz7V8zUngXytSpMOUC7LV2_d65xRThXFKsoUgRaFtthelZK0_PYsUq6HeU47YY1gfRySZQ23-d72t7dw1JCmW_QZ3ccwbLz13C1jeBbzHajRsdNraJoGn1KSSaoJ6yFHR0QBN4NwUeVRS1viKEAAYRwJfcUWWx33HfmfTOkh4yssnf7FoSIPggPt-A2rKYwjUR8OWaDdvBNkydoZTycWO2aAA9FOjbJj-l7_Fq4KbQ9Oj-7UODNbNeHKSOcwaah5xgr7r--54InP3ZHK7CzdweK3UewzDM7NGa7_V63piCqig2i_j9ygQPnsLR_raLah1cRNBGwg5ge-wEBZN2ovIz6xxnZ-d0pBVrv_wqHd3G_5IQbjISubix9mpd-TMRt8I9Jsrd9LSkf0iXitwtAr6AHiBZ-GX3IJDEWiV7gc9aHjrX3JFYl_pE"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.api+json",
    "X-Trace-Id": str(uuid.uuid4())
}

class TestAttachmentsAPI(unittest.TestCase):

    def test_list_attachments_success(self):
        response = requests.get(BASE_URL, headers=HEADERS, params={"limit": 10, "page": 1})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)
        self.assertIn("meta", data)
        self.assertIn("pagination", data["meta"])

    def test_unauthenticated_request(self):
        response = requests.get(BASE_URL, headers={"Accept": "application/vnd.api+json"})
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertTrue(data.get("message", "").startswith("Unauthenticated"))

    def test_invalid_page_parameter(self):
        response = requests.get(BASE_URL, headers=HEADERS, params={"page": "invalid"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)

    def test_page_not_found(self):
        response = requests.get(BASE_URL, headers=HEADERS, params={"page": 99999})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data.get("data", [])), 0)

    def test_trace_id_in_header(self):
        trace_id = str(uuid.uuid4())
        headers = HEADERS.copy()
        headers["X-Trace-Id"] = trace_id
        response = requests.get(BASE_URL, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.headers.get("X-Trace-Id"), trace_id)

if __name__ == "__main__":
    unittest.main()
