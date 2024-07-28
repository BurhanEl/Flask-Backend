class DataProvider():
  def __init__(self, host, user, pwd, db) -> None:
    pass
  
  def check_duplicate(self, data) -> bool:
    raise NotImplementedError
  
  def store_salary(self, salary, id) -> None:
    raise NotImplementedError

  def run_query(self, cursor, query, select=False, commit=False, close=True) -> None:
    raise NotImplementedError

  def get(self, or_data) -> None:
    raise NotImplementedError

  def put(self, or_data, condition_column="id") -> dict:
    raise NotImplementedError

  def post(self, or_data) -> dict:
    raise NotImplementedError
  
  def delete(self, or_data) -> dict:
    raise NotImplementedError
  
  def cal_salary_from_hours(self, hours, emp_id) -> None:
    raise NotImplementedError

  def cal_salary_from_wages(self, wages, emp_id) -> None:
    raise NotImplementedError
  