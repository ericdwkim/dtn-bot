import unittest
from utility import setup_driver, teardown_driver


class TestDriver(unittest.TestCase):
    def setUp(self):
        self.driver = setup_driver()

    def tearDown(self):
        teardown_driver(self.driver)
    #

    def test_driver_setup_and_teardown(self):
        # Test setup and teardown of driver instance
        self.assertTrue(is_initialized(self.driver))
        self.assertTrue(is_connected(self.driver))

if __name__ == '__main__':
    unittest.main()
