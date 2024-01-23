import app
import unittest


class TestRoutes(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_home_get_route_response_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_route_get_response_code(self):
        response = self.app.get('/create')
        self.assertEqual(response.status_code, 200)
