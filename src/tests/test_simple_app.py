import unittest
import tracemalloc

tracemalloc.start()

from app import app

class Test_Simple(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        hello = response.get_data(as_text=True)
        assert "Hello World!" == response.get_data(as_text=True)

    
    def test_help(self):
        with self.client.get('/help') as response:
            assert response.status_code == 200
            gen_response = response.get_data(as_text=True)


        with self.client.get('/transactions/help') as response:
            assert response.status_code == 200

        with self.client.get('/patients/help') as response:
            assert response.status_code == 200

        with self.client.get('/pharmacies/help') as response:
            assert response.status_code == 200 

        with self.client.get('/doesnotexist/help') as response:
            assert response.status_code == 200
            assert response.get_data(as_text=True) == gen_response

if __name__ == "__main__":
    unittest.main()