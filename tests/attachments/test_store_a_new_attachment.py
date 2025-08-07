import unittest
import requests
import uuid

class TestCreateAttachment(unittest.TestCase):
    BASE_URL = "http://localhost:8080/api/v1/attachments"
    TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZGQ4NzhiMDhlYzI3YzFkZTcwYmUyNjI1MDRiZTg1N2M0MTdiMDQ4YzdlZjNjMDA3YmNmZWNmNTM1NGJmNDdlZGNhZDczNDIyOTk0M2U2ZjMiLCJpYXQiOjE3NTQyMTE0NTAuNzE0MzA2LCJuYmYiOjE3NTQyMTE0NTAuNzE0MzEzLCJleHAiOjE3ODU3NDc0NDkuNDAzNDQ4LCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.PDVe2nJpSRA8EdKUX2QalQjROp0rOjp94n1jR7xR12mX_bFmJAmqIGgXIIFMghEtMIw6exBedJ6_FlAYs0sDBPXnFSfKuEyNNrKGbwjV1XJktFjZvL1okg5OF2g7_pM6qH5CCjz9p0nHvQ5QnMMRBw-Z38GUhZbzF1jm49VtHk2J0_7nk8ko4C9dpRzkR2LemtivntAW8mgzQNJxVElmVQfOO4UNsiDZ8aDV6V1R0JjK_e29yf73AXz7V8zUngXytSpMOUC7LV2_d65xRThXFKsoUgRaFtthelZK0_PYsUq6HeU47YY1gfRySZQ23-d72t7dw1JCmW_QZ3ccwbLz13C1jeBbzHajRsdNraJoGn1KSSaoJ6yFHR0QBN4NwUeVRS1viKEAAYRwJfcUWWx33HfmfTOkh4yssnf7FoSIPggPt-A2rKYwjUR8OWaDdvBNkydoZTycWO2aAA9FOjbJj-l7_Fq4KbQ9Oj-7UODNbNeHKSOcwaah5xgr7r--54InP3ZHK7CzdweK3UewzDM7NGa7_V63piCqig2i_j9ygQPnsLR_raLah1cRNBGwg5ge-wEBZN2ovIz6xxnZ-d0pBVrv_wqHd3G_5IQbjISubix9mpd-TMRt8I9Jsrd9LSkf0iXitwtAr6AHiBZ-GX3IJDEWiV7gc9aHjrX3JFYl_pE"

    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "X-Trace-Id": str(uuid.uuid4()),
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/json"
    }

    VALID_ATTACHABLE_ID = "1"  # שים כאן מזהה תקף לפי מה שקיים אצלך
    VALID_ATTACHABLE_TYPE = "Bill"  # ודא שסוג זה קיים

    def test_create_attachment_success(self):
        payload = {
            "filename": "file.pdf",
            "attachable_type": self.VALID_ATTACHABLE_TYPE,
            "attachable_id": self.VALID_ATTACHABLE_ID,
            "title": "Some PDF file",
            "notes": "Some notes"
        }

        response = requests.post(self.BASE_URL, headers=self.HEADERS, json=payload)
        print("SUCCESS response:", response.status_code, response.text)

        if response.status_code == 422:
            self.skipTest("attachable_id לא תקף. דלג על הבדיקה עד שתהיה ישות קיימת.")

        self.assertEqual(response.status_code, 200)

        json_data = response.json()
        self.assertIn("data", json_data)
        self.assertEqual(json_data["data"]["attributes"]["filename"], "file.pdf")
        self.assertEqual(json_data["data"]["attributes"]["attachable_type"], self.VALID_ATTACHABLE_TYPE)
        self.assertEqual(json_data["data"]["attributes"]["attachable_id"], self.VALID_ATTACHABLE_ID)

    def test_create_attachment_unauthorized(self):
        headers = self.HEADERS.copy()
        headers["Authorization"] = "Bearer INVALID_TOKEN"

        payload = {
            "filename": "file.pdf",
            "attachable_type": self.VALID_ATTACHABLE_TYPE,
            "attachable_id": self.VALID_ATTACHABLE_ID,
            "title": "Some PDF file",
            "notes": "Some notes"
        }

        response = requests.post(self.BASE_URL, headers=headers, json=payload)
        print("UNAUTHORIZED response:", response.status_code, response.text)

        self.assertEqual(response.status_code, 401)
        self.assertIn("Unauthenticated", response.json()["message"])

    def test_create_attachment_validation_error(self):
        payload = {
            "filename": "",
            "attachable_type": ""
        }

        response = requests.post(self.BASE_URL, headers=self.HEADERS, json=payload)
        print("VALIDATION ERROR response:", response.status_code, response.text)

        self.assertEqual(response.status_code, 422)
        self.assertIn("message", response.json())
        self.assertIn("errors", response.json())
        self.assertTrue(any("filename" in k or "attachable_type" in k for k in response.json()["errors"]))

if __name__ == '__main__':
    unittest.main()
