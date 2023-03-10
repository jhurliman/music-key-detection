import os
import unittest
import index

from base64 import b64encode


class TestHandlerCase(unittest.TestCase):
    def test_empty_request(self):
        print("testing empty request.")
        result = index.handler(None, None)
        print(result)
        self.assertEqual(result["statusCode"], 400)
        self.assertEqual(result["headers"]["Content-Type"], "application/json")
        self.assertIn("error", result["body"])

    def test_missing_filename(self):
        print("testing missing filename.")
        result = index.handler({"content": "foo"}, None)
        print(result)
        self.assertEqual(result["statusCode"], 400)
        self.assertEqual(result["headers"]["Content-Type"], "application/json")
        self.assertIn("error", result["body"])

    def test_key_detection(self):
        filename = "preludeincmajor-30s.mp3"
        filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
        print(f"testing key detection for {filepath}.")
        # load the mp3 into a base64 encoded string
        with open(filepath, "rb") as f:
            content = f.read()
        base64_content = b64encode(content)
        result = index.handler({"filename": filename, "content": base64_content}, None)
        print(result)
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["headers"]["Content-Type"], "application/json")
        self.assertIn("key", result["body"])
        self.assertIn("scale", result["body"])


if __name__ == "__main__":
    unittest.main()
