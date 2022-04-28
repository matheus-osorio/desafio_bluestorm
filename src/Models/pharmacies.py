from src.Models.utils import verifier, insert_uuid, make_params_array

class Pharmacies:
  @verifier(
    {
      'uuid': {'type': 'str', 'verification': 'string'},
      'name': {'type': 'str', 'verification': 'string'},
      'city': {'type': 'str', 'verification': 'string'}
    }
  )
  def select(self, parameters: dict) -> [str, list, list]:
    names = ['uuid', 'name', 'city']
    params = make_params_array(parameters, names)
    query = f''' 
    select {','.join(names)}
    from pharmacies
    where
    1 = 1
    {f"and uuid = ?" if 'uuid' in parameters else ''}
    {f"and name = ?" if 'name' in parameters else ''}
    {f"and city = ?" if 'city' in parameters else ''}
    ;
    '''
    return query, names, params
  
  @verifier(
    {
      'name': {'type': 'str', 'verification': 'string', 'obligatory': True},
      'city': {'type': 'str', 'verification': 'string', 'obligatory': True}
    }
  )
  @insert_uuid
  def insert(self, parameters: dict) -> [str, list]:
    names = ['uuid', 'name', 'city']
    params = make_params_array(parameters, names)
    return f''' 
    insert into pharmacies ({','.join(names)})
    values (?,?,?);
    ''', params
  
  def __getitem__(self, name: str) -> callable: # ensures we can access the values of this class via instance['function_name'] method
    return getattr(self, name)

