import requests
import json
import re

class SDK:
  def __init__(self, base_address: str, username: str = None, password: str = None) -> None:
    if base_address[-1] != '/':
      base_address = base_address + '/'
    self.sdk_version = '1.0.0'
    self.base_address = base_address


    if username == None or password == None:
      self.allow_use = False
    else:
      self.auth = {
        'username': username,
        'password': password
      }
      self.allow_use = True
  
  def test(self) -> None:
    try:
      response = requests.request('get', self.base_address)
    except:
      return False
    return response.status_code == 200
  
  def check_sdk(self) -> None:
    try:
      response = requests.request('get', self.base_address + 'sdk')
      obj = json.loads(response.content)
      expected_version = obj['version']
      expected_version_regex = expected_version.replace('.','\.').replace('x', '\d+')
      return re.search(expected_version_regex, self.sdk_version) is not None
    except:
      return False

  def select(self, table: str, param_list: dict = {}) -> dict:
    if not self.allow_use:
      raise ValueError('No authorization values found!')
    filter_list = []
    if table == 'patients':
      filter_list = ['first_name', 'last_name', 'date_of_birth', 'uuid']
    elif table == 'pharmacies':
      filter_list = ['name', 'city', 'uuid']
    elif table == 'transactions':
      filter_list = ['patient_uuid',
      'patient_first_name',
      'patient_last_name',
      'patient_birthday',
      'pharmacy_uuid',
      'pharmacy_name',
      'pharmacy_city',
      'transaction_uuid',
      'transaction_amount',
      'transaction_timestamp'
      ]
    else:
      raise ValueError("table parameter must be 'patients', 'pharmacies' or 'transactions'")

    for name in param_list:
      if name not in filter_list:
        print(f'WARNING: PARAMETER {name} IS NOT ACCEPTED')
    
    try:
      response = requests.request('get', self.base_address + table, params = param_list,headers = self.auth)
      return json.loads(response.content)
    except:
      raise ConnectionError('Something went wrong')
  
  def insert(self, table: str, value_list: dict) -> dict:
    if not self.allow_use:
      raise ValueError('No authorization values found!')

    if table == 'patients':
      param_list = ['first_name', 'last_name', 'date_of_birth']
    elif table == 'pharmacies':
      param_list = ['name', 'city']
    elif table == 'transactions':
      param_list = ['patient_uuid', 'pharmacy_uuid', 'timestamp', 'amount']      
    else:
      raise ValueError("table parameter must be 'patients', 'pharmacies' or 'transactions'")

    for name in param_list:
      if name not in value_list:
        raise ValueError(f'The parameter {name} is necessary for insertion!')
    
    try: 
      response = requests.request('post', self.base_address + table + '/insert', headers = self.auth, json = value_list)
      return json.loads(response.content)
    except:
      raise ConnectionError('Something Went Wrong')

