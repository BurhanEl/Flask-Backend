from data_provider import *
import mysql.connector
from flask import jsonify

class MySQLDataProvider(DataProvider):
  def __init__(self, host, user, pwd, db) -> None:
    self.conn = mysql.connector.connect(
      host=host,
      user=user,
      password=pwd,
      database=db
    )
  
  def check_duplicate(self, data) -> bool:
    cursor = self.conn.cursor()
    table = data["table"]
    del data["table"]

    query = f"SELECT * FROM {table} WHERE "

    for key in data:
      if type(data[key]) == str:
        query += f"{key}='{data[key]}' AND "
      else:
        query += f"{key}={data[key]} AND "

    query = query[:-5]
    record = self.run_query(cursor, query, select=True)
    return len(record) != 0
  
  def store_salary(self, salary, id) -> None:
    salary_data = {
      "table": "salary",
      "employee_id": id,
      "base_salary": salary
    }
    dup_data = salary_data.copy()
    del dup_data["base_salary"]
    if self.check_duplicate(dup_data):
      salary_data["id"] = salary_data["employee_id"]
      del salary_data["employee_id"]
      self.put(salary_data, condition_column="employee_id")
    else:
      self.post(salary_data)

  def run_query(self, cursor, query, select=False, commit=False, close=True) -> None:
    cursor.execute(query)
    if select:
      data = []
      for row in cursor.fetchall():
        data.append(row)  
      return data
    if commit:
      self.conn.commit()
    if close:
      cursor.close()

  def get(self, or_data) -> None:
    cursor = self.conn.cursor()

    table = or_data["table"]
    del or_data["table"]

    query = f"SELECT * FROM {table}"

    if len(or_data) > 0:
      query += " WHERE "
      for key in or_data:
          if type(or_data[key]) == str:
            query += f"{key}='{or_data[key]}' AND "
          else:
            query += f"{key}='{or_data[key]}' AND "
      
      query = query[:-5]
    return self.run_query(cursor, query, select=True)

  def put(self, or_data, condition_column="id") -> dict:
    cursor = self.conn.cursor()
    table = or_data["table"]
    id  = or_data["id"]
    del or_data["table"]
    del or_data["id"]

    query = f"UPDATE {table} SET "

    for key in or_data:
      if type(or_data[key]) != str:
          query += f"{key}={or_data[key]}, "
      else:
          query += f"{key}='{or_data[key]}', "
    
    query = query[:-2]
    query += f" WHERE {condition_column}={id}"
    self.run_query(cursor, query, commit=True)
    
    return jsonify({
      "status_code": 200,
      "message": "Updated"
    })

  def post(self, or_data) -> dict:
    cursor = self.conn.cursor()
    table = or_data["table"]
    del or_data["table"]

    data = {}
    data1 = {}

    for i in or_data:
      if type(or_data[i]) != str:
        data1[i] = or_data[i]
      else:
        data[i] = or_data[i]
    
    if len(data1) == 0:
      query = f"insert into {table} ({", ".join(k for k in list(data.keys()))}) values ('{"', '".join(str(data[k]) for k in list(data.keys()))}')"
    elif len(data)==0:
      query = f"insert into {table} ({", ".join(k for k in list(data1.keys()))}) values ({", ".join(str(data1[k]) for k in list(data1.keys()))})"
    else:
      query = f"insert into {table} ({", ".join(k for k in list(data.keys()))}, {", ".join(k for k in list(data1.keys()))}) values ('{"', '".join(str(data[k]) for k in list(data.keys()))}', {", ".join(str(data1[k]) for k in list(data1.keys()))})"
    
    self.run_query(cursor, query, commit=True, close=False)

    query2 = f"SELECT * FROM {table} ORDER BY id DESC LIMIT 1"

    or_data["table"] = table
    return {
       "Data": self.run_query(cursor, query2, select=True)
    }
  
  def delete(self, or_data) -> dict:
    cursor = self.conn.cursor()
    table = or_data["table"]
    id  = or_data["id"]
    del or_data["table"]
    del or_data["id"]
    # value =  (data['id'],)
    query2 = f"DELETE FROM {table} WHERE id = {id}"
    # print(query2)
    self.run_query(cursor, query2, commit=True)
    return jsonify({
      "status_code": 200,
      "message": "Deleted"
    })
  
  def cal_salary_from_hours(self, hours, emp_id):
    wages = self.get({
    "table": "wages",
    "employee_id": emp_id
    })
  # print("Fetched hours data:", hours)

    if wages:
        # hours_worked = hours[0][2]
        hourly_wage = wages[0][2]
        print("Hours worked:", hourly_wage)

        time = int(hourly_wage)
        base_salary = time * hours
        self.store_salary(base_salary, emp_id)  

  def cal_salary_from_wages(self, wages, emp_id):
    hours = self.get({
    "table": "hours",
    "employee_id": emp_id
    })
  # print("Fetched hours data:", hours)
    if hours:
        # hours_worked = hours[0][2]
        hours_worked = hours[0][2]
        print("Hours worked:", hours_worked)
        time = int(hours_worked)
        base_salary = time * wages
        self.store_salary(base_salary, emp_id)    
