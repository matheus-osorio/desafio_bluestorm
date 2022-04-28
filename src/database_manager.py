import sqlite3
from src.Models.patients import Patients
from src.Models.pharmacies import Pharmacies
from src.Models.transactions import Transactions
from src.Models.users import Users

class Database_Manager:
  instance = None
  
  def __init__(self, filename: str = None):
    self.filename = filename
    self.connection = sqlite3.connect(filename)
    self.cursor = self.connection.cursor()
  
  def run(self, query: str, params: list) -> sqlite3:
    return self.cursor.execute(query, params)
  
  def make_row_names(self, results: [list], names: list) -> [dict]:
    arr = []
    for row in results:
      obj = {}
      for enum in enumerate(names):
        index, name = enum
        obj[name] = row[index]
      arr.append(obj)
    return arr

  def authorization(self, parameters: dict) -> bool:
    model = Users()
    
    query,_, params = model.select(parameters)
    results = self.run(query, params).fetchall()
    return len(results) > 0
    

  def select(self, table, parameters):
    if table == 'users':
      return self.authorization(parameters)

    if table == 'pharmacies':
      model = Pharmacies()
    elif table == 'patients':
      model = Patients()
    elif table == 'transactions':
      model = Transactions()

    query, names, params = model.select(parameters)
    results = self.run(query, params).fetchall()
    return self.make_row_names(results, names)
  
  def insert(self, table, parameters):
    if table == 'users':
      model = Users()
    elif table == 'pharmacies':
      model = Pharmacies()
    elif table == 'patients':
      model = Patients()
    elif table == 'transactions':
      model = Transactions() 
    
    query, param_list = model.insert(parameters)

    results = self.run(query, param_list)
    
    self.connection.commit()
    return parameters

  def __getitem__(self, name):
    return getattr(self, name)



