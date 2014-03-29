from mock import Mock
from models import BikeStache
import app as bikestache
import json
import unittest


class AppTestCase(unittest.TestCase):

    def test_get_stache_return_stache(self):
        bikestache.find_closest_stache = Mock(
            return_value=BikeStache('test', 0, 0))
        self.app = bikestache.app.test_client()

        data = dict(latitude=37.7578357, longitude=-122.451142)

        response = self.app.post('/get_stache', method='POST', data=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertNotEquals(response_data['stache'], None)

    def test_get_stache_none_in_range(self):
        bikestache.find_closest_stache = Mock(return_value=None)
        self.app = bikestache.app.test_client()

        data = dict(latitude=39.1463584, longitude=-94.5708061)

        response = self.app.post('/get_stache', method='POST', data=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['stache'], None)

    def test_get_stache_invalid_coordinates(self):
        self.app = bikestache.app.test_client()

        data = dict(latitude=-1, longitude=-181)

        response = self.app.post('/get_stache', method='POST', data=data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
