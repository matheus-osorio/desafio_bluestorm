import re
from uuid import uuid4 as uuid

regex_patterns = {
  'int': r'\d+',
  'float': r'\d+\.\d+',
  'number': r'\d+(\.\d+)?',
  'datetime': r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}'
}

def verifier(sanitize: dict) -> callable:
  def decorator(func: callable) -> callable:
    def wrapper(class_instance: object, params: dict) -> any:
      for name in sanitize:
        sanitizer = sanitize[name]

        if 'obligatory' not in sanitizer:
          sanitizer['obligatory'] = False
        
        
        if name not in params and sanitizer['obligatory']:
          raise ValueError(f'Value {name} is missing!')

        if name not in params:
          continue

        
        param = params[name]
        
        if type(param).__name__ != sanitizer['type']:
          raise TypeError(f'Parameter {name} has Wrong Type! Expected: {sanitizer["type"]} Found: {type(param).__name__}')

        if sanitizer['verification'] in regex_patterns:
          verification_name = sanitizer['verification']
          pattern = regex_patterns[verification_name]
          search = re.search(pattern, param)
          if not search:
            raise ValueError(f'Parameter {name} didn\'t pass verification')
          
          if sanitizer['verification'] == 'int':
            params[name] = int(param)

        elif sanitizer['verification'] == 'string':
          param = param.replace("'","\'")
          params[name] = param

      return func(class_instance, params)
    
    return wrapper
  
  return decorator


def insert_uuid(func: callable) -> callable:
  def wrapper(class_instance: object, params: dict) -> any:
    params['uuid'] = str(uuid())
    return func(class_instance, params)
  return wrapper
    

def make_params_array(obj: dict, names: list) -> list:
  arr = []
  for name in names:
    if name in obj:
      arr.append(obj[name])
  return arr

        