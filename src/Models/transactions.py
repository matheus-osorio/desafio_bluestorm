from src.Models.utils import verifier, insert_uuid, make_params_array

class Transactions:

  @verifier(
    {
      'patient_uuid': {'type': 'str', 'verification': 'string'},
      'patient_first_name': {'type': 'str', 'verification': 'string'},
      'patient_last_name': {'type': 'str', 'verification': 'string'},
      'patient_birthday': {'type': 'str', 'verification': 'datetime'},
      'pharmacy_uuid': {'type': 'str', 'verification': 'string'},
      'pharmacy_name': {'type': 'str', 'verification': 'string'},
      'pharmacy_city': {'type': 'str', 'verification': 'string'},
      'transaction_uuid': {'type': 'str', 'verification': 'string'},
      'transaction_amount': {'type': 'str', 'verification': 'int'},
      'transaction_timestamp': {'type': 'str', 'verification': 'datetime'}
    }
  )
  def select(self, parameters: dict) -> [str, list, list]:
    names = ['p.uuid','p.first_name','p.last_name','p.date_of_birth','ph.uuid','ph.name','ph.city','t.uuid','t.amount','t.timestamp']
    param_names = [
    text
    .replace('ph.', 'pharmacy_')
    .replace('t.','transaction_')
    .replace('p.','patient_')
    for text in names
    ]
    params = make_params_array(parameters, param_names)
    query = f''' 
    select 
    {','.join(names)}
    from transactions t
      inner join patients p on t.patient_uuid = p.uuid
      inner join pharmacies ph on t.pharmacy_uuid = ph.uuid
    where
    1=1
    {f"and p.uuid = ?" if 'patient_uuid' in parameters else ''}
    {f"and p.first_name = ?" if 'patient_first_name' in parameters else ''}
    {f"and p.last_name = ?" if 'patient_last_name' in parameters else ''}
    {f"and p.date_of_birth = ?" if 'patient_birthday' in parameters else ''}
    {f"and ph.uuid = ?" if 'pharmacy_uuid' in parameters else ''}
    {f"and ph.name = ?" if 'pharmacy_name' in parameters else ''}
    {f"and ph.city = ?" if 'pharmacy_city' in parameters else ''}
    {f"and t.uuid = ?" if 'transaction_uuid' in parameters else ''}
    {f"and t.amount = ?" if 'transaction_amount' in parameters else ''}
    {f"and t.timestamp = ?" if 'transaction_timestamp' in parameters else ''}
    ;

    '''

    return query, param_names, params
  
  @verifier(
    {
      'patient_uuid': {'type': 'str', 'verification': 'string', 'obligatory': True},
      'pharmacy_uuid': {'type': 'str', 'verification': 'string', 'obligatory': True},
      'amount': {'type': 'str', 'verification': 'int', 'obligatory': True},
      'timestamp': {'type': 'str', 'verification': 'datetime', 'obligatory': True}
    }
  )
  @insert_uuid
  def insert(self, parameters: dict) -> [str, list]:
    names = ['uuid', 'patient_uuid', 'pharmacy_uuid', 'amount', 'timestamp']
    params = make_params_array(parameters, names)
    return f''' 
    insert into transactions ({','.join(names)})
    values (?,?,?,?,?);
    ''', params
  
  def __getitem__(self, name: str) -> callable: # ensures we can access the values of this class via instance['function_name'] method
    return getattr(self, name)

t = Transactions()