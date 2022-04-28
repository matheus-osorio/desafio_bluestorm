import flask
from src.control import Control
from flask import Flask, request
from src.utils import parse_headers, respond
import json
import argparse
import os

app = Flask(__name__)


control = Control('src/backend_test.db')

def authorizer(func):
  def wrapper(*args, **kwargs):
    headers = parse_headers(request.headers)
    try:
      result = control.make_query('users','select', headers)
      if not result:
        return respond(403, {
          'error': 'Authorization failed!'
        })
    except:
      return respond(500, {'message': 'Something went wrong!'})

    return func(*args, **kwargs)
  wrapper.__name__ = func.__name__ # prevents errors caused by having multiple functions with same name
  return wrapper

@app.route('/sdk')
def def_sdk_version():
  return respond(200, {
    'version': '1.x.x'
  })

@app.route('/')
def greeting():
    return respond(200, 'Hello World!')


@app.get('/help')
def get_general_help():
  file_name = 'src/help/general.txt'
  file = open(file_name, 'r')
  text = file.read()
  file.close()
  return respond(200, text)


@app.get('/<table_name>/help')
def get_help(table_name):
  if table_name == 'patients':
    file_name =  'src/help/patient.txt'
  elif table_name == 'pharmacies':
    file_name =  'src/help/pharmacy.txt'
  elif table_name == 'transactions':
    file_name =  'src/help/transaction.txt'
  else:
    file_name = 'src/help/general.txt'
  
  file = open(file_name, 'r')
  text = file.read()
  file.close()
  return respond(200, text)


@app.post('/<table_name>/insert')
@authorizer
def insert_on_table(table_name):
  
  table_list = ['patients', 'transactions', 'pharmacies'] 

  if table_name not in table_list:
    return respond(403, {
      'message': 'Table is not an option'
    })
  body = json.loads(request.data)
  try: 
    query_response = control.make_query(table_name, 'insert', body)
    
    return respond(200, {
      'message': 'Successfully inserted the data',
      'data': query_response
    })
  except TypeError as error:
    return respond(400, {
      'error': str(error)
    })
  except ValueError as error:
    return respond(406, {
      'error': str(error)
    })
  except:
    return respond(500, {
      'error': 'Could not complete search'
    })



@app.get('/<table_name>')
@authorizer
def get_from_table(table_name):
  
  table_list = ['patients', 'transactions', 'pharmacies'] 
  if table_name not in table_list:
    return respond(403, {
      'message': 'Table is not an option!'
    })
  
  data = request.args.to_dict()

  try:
    query_response = control.make_query(table_name, 'select', data)
    return respond(200, {
      'rows': query_response
    })
  except TypeError as error:
    return respond(400, {
      'error': str(error)
    })
  except ValueError as error:
    return respond(406, {
      'error': str(error)
    })
  except:
    return respond(500, {
      'error': 'Could not complete search'
    })


if __name__ == '__main__':
  configs = {
    'host': os.environ['host'],
    'port': os.environ['port'],
    'debug': os.environ['debug'] == '1',
    'use_reloader': os.environ['reloader'] == '1'
  }

  print('configs:', configs)
  app.run(**configs)
  