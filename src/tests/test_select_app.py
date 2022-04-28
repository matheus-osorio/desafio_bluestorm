import unittest
from app import control, app
import shutil
import os

class Test_Select(unittest.TestCase):
  def setUp(self):
    control.filename = 'src/tests/db_mock_copy.db'
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    self.ctx = app.app_context()
    self.ctx.push()
    self.client = app.test_client()
    self.base_name = 'src/tests/mocks/selects/'

  def tearDown(self):
    self.ctx.pop()
  
  @classmethod
  def setUpClass(cls):
    shutil.copy('src/tests/db_mock.db','src/tests/db_mock_copy.db')

  @classmethod
  def tearDownClass(cls):
    os.remove('src/tests/db_mock_copy.db')

  def test_getters(self):
    auth = {
      'username': 'admin',
      'password': 'admin'
    }

    with self.client.get('/patients', headers=auth) as response:
      assert response.status_code == 200
      file_response = open(self.base_name + 'patients_response.json','r')
      expected_response = file_response.read()
      file_response.close()
      assert response.get_data(as_text=True) == expected_response
    
    with self.client.get('/pharmacies', headers=auth) as response:
      assert response.status_code == 200
      file_response = open(self.base_name + 'pharmacies_response.json','r')
      expected_response = file_response.read()
      file_response.close()
      assert response.get_data(as_text=True) == expected_response
    
    with self.client.get('/transactions', headers=auth) as response:
      assert response.status_code == 200
      file_response = open(self.base_name + 'transactions_response.json','r')
      expected_response = file_response.read()
      file_response.close()
      assert response.get_data(as_text=True) == expected_response
    

  
  

