import unittest
from app import control, app
import shutil
import os
import json
import re

class Test_Select(unittest.TestCase):
  def setUp(self):
    control.filename = 'src/tests/db_mock_copy.db'
    app.config['TESTING'] = True
    app.config['DEBUG'] = False
    self.ctx = app.app_context()
    self.ctx.push()
    self.client = app.test_client()
    self.base_name = 'src/tests/mocks/inserts/'

  def tearDown(self):
    self.ctx.pop()
  
  @classmethod
  def setUpClass(cls):
    shutil.copy('src/tests/db_mock.db','src/tests/db_mock_copy.db')

  @classmethod
  def tearDownClass(cls):
    os.remove('src/tests/db_mock_copy.db')

  def test_setters(self):
    auth = {
      'username': 'admin',
      'password': 'admin'
    }
    patient = {
      'first_name': 'JOAO',
      'last_name': 'SILVA',
      'date_of_birth': '1999-10-10 10:10:10.000000'
    }
    with self.client.post('/patients/insert', headers=auth, data=json.dumps(patient)) as response:
      assert response.status_code == 200
      file_response = open(self.base_name + 'patients_response.json','r')
      expected_response = json.loads(file_response.read())
      file_response.close()
      response_obj = json.loads(response.get_data(as_text=True))
      patient_uuid = response_obj['data']['uuid']
      del response_obj['data']['uuid']
      assert re.search(r'^.{8}-.{4}-.{4}-.{4}-.{12}$', patient_uuid) is not None
      assert response_obj == expected_response
    
    pharmacy = {
      'name': 'DROGASIL',
      'city': 'SAO PAULO',
    }

    with self.client.post('/pharmacies/insert', headers=auth, data=json.dumps(pharmacy)) as response:
      assert response.status_code == 200
      file_response = open(self.base_name + 'pharmacies_response.json','r')
      expected_response = json.loads(file_response.read())
      file_response.close()
      response_obj = json.loads(response.get_data(as_text=True))
      pharm_uuid = response_obj['data']['uuid']
      del response_obj['data']['uuid']
      assert re.search(r'^.{8}-.{4}-.{4}-.{4}-.{12}$', pharm_uuid) is not None
      assert response_obj == expected_response

    transaction = {
      'patient_uuid': patient_uuid,
      'pharmacy_uuid': pharm_uuid,
      'amount': '100',
      'timestamp': '1999-10-10 10:10:10.000000'
    }

    with self.client.post('/transactions/insert', headers=auth, data=json.dumps(transaction)) as response:
      assert response.status_code == 200
      file_response = open(self.base_name + 'transactions_response.json','r')
      expected_response = json.loads(file_response.read())
      file_response.close()
      response_obj = json.loads(response.get_data(as_text=True))
      pharm_uuid = response_obj['data']['uuid']
      del response_obj['data']['uuid']
      del response_obj['data']['patient_uuid']
      del response_obj['data']['pharmacy_uuid']
      assert re.search(r'^.{8}-.{4}-.{4}-.{4}-.{12}$', pharm_uuid) is not None
      assert response_obj == expected_response
    

  
  

