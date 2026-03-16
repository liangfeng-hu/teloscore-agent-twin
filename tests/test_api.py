import unittest

from api.app import health, root


class TestAPI(unittest.TestCase):
    def test_root(self):
        data = root()
        self.assertEqual(data["name"], "TelosCore Agent Twin")

    def test_health(self):
        data = health()
        self.assertEqual(data["status"], "ok")


if __name__ == "__main__":
    unittest.main()
