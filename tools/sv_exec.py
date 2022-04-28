#!/usr/bin/env python3

import argparse as ap
import requests
import json

parser = ap.ArgumentParser(allow_abbrev=False, description='This a tool to help you test the server in a compact and organized manner')

subparser = parser.add_subparsers(help='sub-command help', dest='command')

patients_parser = subparser.add_parser('patients', help='holds the subparser values for the patients table')
patients_parser.add_argument('-m', '--method', required=True, choices=['select', 'insert'])
patients_parser.add_argument('-fn', '--firstname', required=False, help='First Name Value', dest='first_name')
patients_parser.add_argument('-ln','--lastname', required=False, help='Last Name Value', dest='last_name')
patients_parser.add_argument('-bd', '--birthday', required=False, help='Birthday Value', dest='date_of_birth')
patients_parser.add_argument('-id','--uuid', required=False, help='UUID (select exclusive)')

pharmacy_parser = subparser.add_parser('pharmacies', help='holds the subparser values for the pharmacies table')
pharmacy_parser.add_argument('-m', '--method', required=True, choices=['select','insert'])
pharmacy_parser.add_argument('-n', '--name', required=False)
pharmacy_parser.add_argument('-c', '--city', required=False)
pharmacy_parser.add_argument('-id','--uuid', required=False)

transaction_parser = subparser.add_parser('transactions', help='holds the subparser values for the transactions table')
transaction_parser.add_argument('-m', '--method', required=True, choices=['select','insert'])
transaction_parser.add_argument('-pat-id', '--patient-uuid', dest='patient_uuid')
transaction_parser.add_argument('-pat-fn', '--patient-firstname', dest='patient_first_name')
transaction_parser.add_argument('-pat-ln', '--patient-lastname', dest='patient_last_name')
transaction_parser.add_argument('-pharm-id', '--pharmacy-uuid', dest='pharmacy_uuid')
transaction_parser.add_argument('-pharm-n', '--pharmacy-name', dest='pharmacy_name')
transaction_parser.add_argument('-pharm-c', '--pharmacy-city',dest='pharmacy_city')
transaction_parser.add_argument('-id', '--transaction-uuid',dest='transaction_uuid')
transaction_parser.add_argument('-a', '--amount', dest='transaction_amount')
transaction_parser.add_argument('-ts', '--timestamp',dest='transaction_timestamp')

configs_parser = subparser.add_parser('config', help='Makes the configuration to use')
configs_parser.add_argument('--url', required=True)
configs_parser.add_argument('--username', required=True)
configs_parser.add_argument('--password', required=True)

user_parser = subparser.add_parser('users')
user_parser.add_argument('--username', required=True)
user_parser.add_argument('--password', required=True)

obj = vars(parser.parse_args())

configs = {}

if(obj['command'] != 'config'):
  file = open('env.json')
  configs = json.loads(file.read())
  file.close()
response = None
if obj['command'] == 'config':
  file = open('env.json','w')
  del obj['command']
  file.write(json.dumps(obj, indent=2))
  file.close()

elif obj['command'] == 'users':
  response = requests.request('post', configs['url'] + 'create', headers = configs, json=obj)

elif obj['command'] == 'transactions':
  if obj['method'] == 'insert':
    obligatory_params = ['pharmacy_uuid', 'patient_uuid', 'transaction_amount', 'transaction_timestamp']
    for param in obligatory_params:
      if param not in obj:
        raise ValueError(f'Missing {param} parameter')
  
    obj['amount'] = obj['transaction_amount']
    del obj['transaction_amount']

    obj['timestamp'] = obj['transaction_timestamp']
    del obj['transaction_timestamp']

    response = requests.request('post', configs['url'] + '/transactions/insert', headers = configs, json=obj)
  else:
    response = requests.request('get', configs['url'] + '/transactions', headers = configs, params = obj)

elif obj['command'] == 'pharmacies':
  if obj['method'] == 'insert':
    obligatory_params = ['name', 'city']
    for param in obligatory_params:
      if param not in obj:
        raise ValueError(f'Missing {param} parameter')

    response = requests.request('post', configs['url'] + '/pharmacies/insert', headers = configs, json=obj)
  else:
    response = requests.request('get', configs['url'] + '/pharmacies', headers = configs, params = obj)

elif obj['command'] == 'patients':
  if obj['method'] == 'insert':
    obligatory_params = ['first_name', 'last_name', 'date_of_birth']
    for param in obligatory_params:
      if param not in obj:
        raise ValueError(f'Missing {param} parameter')

    response = requests.request('post', configs['url'] + '/patients/insert', headers = configs, json=obj)
  else:
    response = requests.request('get', configs['url'] + '/patients', headers = configs, params = obj)


if response is not None:
  print(json.loads(response.content))