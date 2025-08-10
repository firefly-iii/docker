import unittest
import requests
import uuid
from tests.firefly_credentials import get_firefly_credentials


class TestCreateAttachment(unittest.TestCase):
    TOKEN = get_firefly_credentials()["token"]
    BASE_URL = "http://localhost:8080/api/v1/attachments"  # עדכן לפי ה-API שלך
    HEADERS = {
        "Authorization": f"Bearer {TOKEN}",
        "X-Trace-Id": str(uuid.uuid4()),
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/json"
    }

    VALID_ATTACHABLE_ID = "1"  # ודא שיש ישות כזו במערכת שלך
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
        self.assertIn("Unauthenticated", response.json().get("message", ""))

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

        errors = response.json()["errors"]
        self.assertTrue(any(field in errors for field in ["filename", "attachable_type"]))

if __name__ == '__main__':
    unittest.main()
