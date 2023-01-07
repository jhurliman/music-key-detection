import unittest
import index


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
        print(f"testing key detection for {filename}.")
        # load the mp3 into a base64 encoded string
        with open(filename, "rb") as f:
            content = f.read()
        base64_content = content.encode("base64")
        result = index.handler({"filename": filename, "content": base64_content}, None)
        print(result)
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(result["headers"]["Content-Type"], "application/json")
        self.assertIn("key", result["body"])
        self.assertIn("scale", result["body"])


if __name__ == "__main__":
    unittest.main()
