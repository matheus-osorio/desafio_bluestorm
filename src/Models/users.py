from src.Models.utils import verifier, insert_uuid, make_params_array
from hashlib import sha256

class Users:
  @verifier(
    {
      'username': {'type': 'str', 'verification': 'string','obligatory': True},
      'password': {'type': 'str', 'verification': 'string','obligatory': True}
    }
  )
  def select(self, parameters: dict) -> [str, list, list]:
    names = ['username', 'password']
    parameters['password'] = sha256(parameters['password'].encode()).hexdigest()
    params = make_params_array(parameters, ['username', 'password'])
    query = f''' 
    select {','.join(names)}
    from users
    where
    username = ? and
    password = ?
    ;
    '''
    return query, names, params
  
  @verifier(
    {
      'first_name': {'type': 'str', 'verification': 'string'},
      'last_name': {'type': 'str', 'verification': 'string'},
      'date_of_birth': {'type': 'str', 'verification': 'datetime'},
    }
  )
  @insert_uuid
  def insert(self, parameters: dict) -> [str, list]:

    parameters['password'] = sha256(parameters['password'].encode()).hexdigest()
    return f''' 
    insert into pharmacies (uuid, username, password)
    values (
      ?,
      ?
    );
    ''', make_params_array(parameters, ['username', 'password'])
  
  def __getitem__(self, name: str) -> callable: # ensures we can access the values of this class via instance['function_name'] method
    return getattr(self, name)

