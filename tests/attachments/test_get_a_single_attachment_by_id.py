import unittest
import requests
import uuid
from tests.firefly_credentials import get_firefly_credentials

class TestGetAttachmentAPI(unittest.TestCase):
    TOKEN = get_firefly_credentials()["token"]
    BASE_URL = get_firefly_credentials()["base_url"] +"/api/v1/attachments"
    BILLS_URL = get_firefly_credentials()["base_url"] +"/api/v1/bills"

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

        attachable_id = bills_data[0].get("id")

        unique_name = f"file_{uuid.uuid4()}.pdf"

        metadata = {
            "name": unique_name,              # שם ייחודי כדי למנוע שגיאת "name already in use"
            "type": "attachment",             # סוג תקין כפי שמצופה מה-API (בדוק תיעוד אם צריך אחרת)
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
