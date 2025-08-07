import unittest
import requests
import uuid

class TestGetAttachmentAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8080/api/v1/attachments"
    BILLS_URL = "http://localhost:8080/api/v1/bills"  # או URL אחר לפי ה-API שלך
    TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZGQ4NzhiMDhlYzI3YzFkZTcwYmUyNjI1MDRiZTg1N2M0MTdiMDQ4YzdlZjNjMDA3YmNmZWNmNTM1NGJmNDdlZGNhZDczNDIyOTk0M2U2ZjMiLCJpYXQiOjE3NTQyMTE0NTAuNzE0MzA2LCJuYmYiOjE3NTQyMTE0NTAuNzE0MzEzLCJleHAiOjE3ODU3NDc0NDkuNDAzNDQ4LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.PDVe2nJpSRA8EdKUX2QalQjROp0rOjp94n1jR7xR12mX_bFmJAmqIGgXIIFMghEtMIw6exBedJ6_FlAYs0sDBPXnFSfKuEyNNrKGbwjV1XJktFjZvL1okg5OF2g7_pM6qH5CCjz9p0nHvQ5QnMMRBw-Z38GUhZbzF1jm49VtHk2J0_7nk8ko4C9dpRzkR2LemtivntAW8mgzQNJxVElmVQfOO4UNsiDZ8aDV6V1R0JjK_e29yf73AXz7V8zUngXytSpMOUC7LV2_d65xRThXFKsoUgRaFtthelZK0_PYsUq6HeU47YY1gfRySZQ23-d72t7dw1JCmW_QZ3ccwbLz13C1jeBbzHajRsdNraJoGn1KSSaoJ6yFHR0QBN4NwUeVRS1viKEAAYRwJfcUWWx33HfmfTOkh4yssnf7FoSIPggPt-A2rKYwjUR8OWaDdvBNkydoZTycWO2aAA9FOjbJj-l7_Fq4KbQ9Oj-7UODNbNeHKSOcwaah5xgr7r--54InP3ZHK7CzdweK3UewzDM7NGa7_V63piCqig2i_j9ygQPnsLR_raLah1cRNBGwg5ge-wEBZN2ovIz6xxnZ-d0pBVrv_wqHd3G_5IQbjISubix9mpd-TMRt8I9Jsrd9LSkf0iXitwtAr6AHiBZ-GX3IJDEWiV7gc9aHjrX3JFYl_pE"

    def setUp(self):
        self.headers = {
            "Authorization": f"Bearer {self.TOKEN}",
            "Accept": "application/vnd.api+json",
            "X-Trace-Id": str(uuid.uuid4())
        }

        # קבלת רשימת bills כדי למצוא attachable_id תקין
        bills_response = requests.get(self.BILLS_URL, headers=self.headers)
        self.assertEqual(bills_response.status_code, 200, "Failed to get bills list")
        bills_data = bills_response.json().get("data", [])
        self.assertTrue(len(bills_data) > 0, "No bills found in system")

        # בוחר את ה-ID של ה-bill הראשון (למשל)
        attachable_id = bills_data[0].get("id")

        metadata = {
            "filename": "file.pdf",
            "attachable_type": "Bill",
            "attachable_id": attachable_id,
            "title": "Test File",
            "notes": "Created for test_get_attachment"
        }

        response = requests.post(self.BASE_URL, headers=self.headers, json=metadata)

        if response.status_code != 200:
            print("POST /attachments failed:")
            print("Status code:", response.status_code)
            print("Response body:", response.text)

        self.assertEqual(response.status_code, 200, "Failed to create attachment in setUp")
        self.attachment_id = response.json()["data"]["id"]

    def test_get_attachment_success(self):
        url = f"{self.BASE_URL}/{self.attachment_id}"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json().get("data", {})
        self.assertEqual(data.get("type"), "attachments")
        self.assertEqual(data.get("id"), self.attachment_id)
        self.assertIn("attributes", data)

    def test_get_attachment_not_found(self):
        url = f"{self.BASE_URL}/999999999"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Resource not found", response.text)

    def test_get_attachment_unauthorized(self):
        url = f"{self.BASE_URL}/{self.attachment_id}"
        bad_headers = {
            "Accept": "application/vnd.api+json",
            "X-Trace-Id": str(uuid.uuid4())
        }
        response = requests.get(url, headers=bad_headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthenticated", response.text)


if __name__ == "__main__":
    unittest.main()
