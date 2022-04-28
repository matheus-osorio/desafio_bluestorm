from src.Models.utils import verifier, insert_uuid, make_params_array

class Patients:
  @verifier(
    {
      'uuid': {'type': 'str', 'verification': 'string'},
      'first_name': {'type': 'str', 'verification': 'string'},
      'last_name': {'type': 'str', 'verification': 'string'},
      'date_of_birth': {'type': 'str', 'verification': 'datetime'},
    }
  )
  def select(self, parameters: dict) -> [str, list, list]:
    names = ['uuid', 'first_name', 'last_name', 'date_of_birth']
    params = make_params_array(parameters, names)
    query = f''' 
    select {','.join(names)}
    from patients
    where
    1 = 1
    {f"and uuid = ?" if 'uuid' in parameters else ''}
    {f"and first_name = ?" if 'first_name' in parameters else ''}
    {f"and last_name = ?" if 'last_name' in parameters else ''}
    {f"and date_of_birth = ?" if 'date_of_birth' in parameters else ''}
    ;
    '''
    return query, names, params
  
  @verifier(
    {
      'first_name': {'type': 'str', 'verification': 'string', 'obligatory': True},
      'last_name': {'type': 'str', 'verification': 'string', 'obligatory': True},
      'date_of_birth': {'type': 'str', 'verification': 'datetime', 'obligatory': True},
    }
  )
  @insert_uuid
  def insert(self, parameters: dict) -> [str, object]: 
    names = ['uuid', 'first_name', 'last_name', 'date_of_birth']
    params = make_params_array(parameters, names)
    return f''' 
    insert into patients ({','.join(names)})
    values (?,?,?,?);
    ''', params
  
  def __getitem__(self, name: str) -> callable: # ensures we can access the values of this class via instance['function_name'] method
    return getattr(self, name)

