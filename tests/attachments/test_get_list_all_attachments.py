import unittest
import requests
import uuid

from tests.firefly_credentials import get_firefly_credentials


TOKEN = get_firefly_credentials()["token"]
BASE_URL = get_firefly_credentials()["base_url"]+"/api/v1/attachments"
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
