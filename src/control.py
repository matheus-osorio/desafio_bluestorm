from src.database_manager import Database_Manager

class Control:

  instance = None

  def __new__(cls, *args): # ensures Singleton Project Pattern 
    if Control.instance is None:
      Control.instance = object.__new__(cls)
    return Control.instance
  
  def __init__(self, filename: str) -> None:
    self.filename = filename

  def create_manager(self) -> Database_Manager:
    return Database_Manager(self.filename)
  
  def make_query(self, query_name: str, operation: str, query_parameters: dict) -> any:
    manager = self.create_manager()
    return manager[operation](query_name, query_parameters)
