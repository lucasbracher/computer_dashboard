from api import api
import unittest


class Test(unittest.TestCase):
    def test_listing_processes(self):
        result = api.output_data()
        self.assertEqual(result["status"], "ok")

    def test_cpu_percentage(self):
        result = api.output_data()
        self.assertGreaterEqual(result["data"]["cpu"], 0.0)


# unittest.main()
