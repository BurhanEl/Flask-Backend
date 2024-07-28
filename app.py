from flask import Flask, request
from mysql_dataprovider import *
from mongo_dataprovider import *
import json

app = Flask(__name__)
config = json.loads(open("config.json").read())

if config["source"] == "mysql":
  data_provider = MySQLDataProvider(
    host=config["host"], 
    user=config["user"],
    pwd=config["pwd"],
    db=config["db"]
  )
else:
  data_provider = MongoDataProvider(
      host=config["host"],
      db=config["db"],
  )

# GET
@app.route('/employees', methods=["GET"])
def getEmployees():
  or_data=request.get_json()
  or_data["table"] = "employee"
  employees = data_provider.get(or_data)
  return employees

@app.route('/jobs', methods=["GET"])
def getjobs():
  or_data=request.get_json()
  or_data["table"] = "job"
  # Execute a query
  jobs=data_provider.get(or_data)
  return jobs

@app.route('/salaries', methods=["GET"])
def getsalaries():
  or_data=request.get_json()
  or_data["table"] = "salary"
  # Execute a query
  jobs=data_provider.get(or_data)
  return jobs

@app.route('/hours', methods=["GET"])
def gethours():
  or_data=request.get_json()
  or_data["table"] = "hours"
  # Execute a query
  jobs=data_provider.get(or_data)
  return jobs

@app.route('/wages', methods=["GET"])
def getwages():
  or_data=request.get_json()
  or_data["table"] = "wages"
  # Execute a query
  jobs=data_provider.get(or_data)
  return jobs

# ==========================================================
# POST
@app.route('/employees', methods=["POST"])
def postEmployees():
  or_data=request.get_json()
  or_data["table"] = "employee"
  try:
    dup_data = {"table": "employee"}
    for key in ["first_name", "last_name", "age"]:
      dup_data[key] = or_data[key]
    if data_provider.check_duplicate(dup_data):
      return {
        "ERROR": "DUPLICATE"
      }
    else:
      employees = data_provider.post(or_data)
  except Exception as e: 
    return{
      "Check":"Documentation",
      "error":print(e)
    }
  return employees

@app.route('/jobs', methods=["POST"])
def postjobs():
  or_data=request.get_json()
  or_data["table"] = "job"
  try:
    dup_data = {"table": "job"}
    dup_data["employee_id"] = or_data["employee_id"]
    if data_provider.check_duplicate(dup_data):
      return {
        "ERROR": "DUPLICATE"
      }
    else:
      jobs = data_provider.post(or_data)
  except Exception as e:
    return{
      "CHECK": f"Documentation {e}"
    }
  return jobs

@app.route('/hours', methods=["POST"])
def posthours():
    or_data=request.get_json()
    or_data["table"] = "hours"
    # try:
    dup_data = {"table": "hours"}
    dup_data["employee_id"] = or_data["employee_id"]
    if data_provider.check_duplicate(dup_data):
      return {
        "ERROR": "DUPLICATE"
      }
    else:
      employees = data_provider.post(or_data)
      hours = or_data["hours_worked"]
      # print("Fetched hours data:", hours)
      employee_id=or_data["employee_id"]
      data_provider.cal_salary_from_hours(hours,employee_id)
    return employees

@app.route('/wages', methods=["POST"])
def postwages():
    or_data = request.get_json()
    or_data["table"] = "wages"
    # Check for duplicates
    dup_data = {"table": "wages"}
    dup_data["employee_id"] = or_data["employee_id"]
    if data_provider.check_duplicate(dup_data):
        return {
            "ERROR": "DUPLICATE"
        }
    else:
        employees = data_provider.post(or_data)
        wage = or_data["hourly_wage"]
        employee_id=or_data["employee_id"]
        data_provider.cal_salary_from_wages(wage,employee_id)
    return employees


# =======================================================================
# PUT
@app.route('/employees', methods=["PUT"])
def putEmployees():
  or_data = request.get_json()
  or_data["table"] = "employee"
  try:
    dup_data = {"table": "employee"}
    dup_data["id"] = or_data["id"]
    if data_provider.check_duplicate(dup_data):
      employees = data_provider.put(or_data)
    else:
      return {
        "ERROR 404": "nothing to update"
      } 
  except Exception as e:
    return {
      "CHECK ":"DOCUMENTATION",
      "error" :print(e)
    }
  # return employees
  return employees

@app.route('/jobs', methods=["PUT"])
def putjobs():
  or_data = request.get_json()
  or_data["table"] = "job"
  try:
    dup_data = {"table": "job"}
    dup_data["id"] = or_data["id"]
    if data_provider.check_duplicate(dup_data):
      employees = data_provider.put(or_data)
    else:
      return {
        "ERROR 404": "nothing to update"
      } 
  except:
    return {
      "CHECK ":"DOCUMENTATION"
    }
  # return employees
  return employees

@app.route('/hours', methods=["PUT"])
def puthours():
  or_data = request.get_json()
  or_data["table"] = "hours"
  try:
    dup_data = {"table": "hours"}
    dup_data["employee_id"] = or_data["employee_id"]
    if data_provider.check_duplicate(dup_data):
      employees = data_provider.put(or_data)

      hours = or_data["hours_worked"]
      employee_id=or_data["employee_id"]
      data_provider.cal_salary_from_hours(hours,employee_id)
    # Fetch hours worked  
    else:
      return {
        "ERROR 404": "nothing to update"
      } 
  except Exception as e:
    return {
      "CHECK ":f"DOCUMENTATION {e}"
    }
  return employees

@app.route('/wages', methods=["PUT"])
def putwages():
  or_data = request.get_json()
  or_data["table"] = "wages"
  try:
    dup_data = {"table": "wages"}
    dup_data["employee_id"] = or_data["employee_id"]
    if data_provider.check_duplicate(dup_data):
      employees = data_provider.put(or_data)
      wage = or_data["hourly_wage"]
      employee_id=or_data["employee_id"]
      data_provider.cal_salary_from_wages(wage,employee_id)
      # Fetch hours worked
    else:
      return {
        "ERROR 404": "nothing to update"
      } 
  except Exception as e:
    return {
      "CHECK ":f"DOCUMENTATION {e}"
    }
  return employees


# +++++++++++======================================================
# DELETE

@app.route('/employees', methods=["DELETE"])
def deleteEmployees():
  or_data = request.get_json()
  or_data["table"] = "employee"
  try:
    dup_data = {"table": "employee"}
    dup_data["id"] = or_data["id"]
    if data_provider.check_duplicate(dup_data):
      employees = data_provider.delete(or_data)
    else:
      return {
        "ERROR 404": "nothing to delete"
      } 
  except Exception as e:
    return {
      "CHECK ":"DOCUMENTATION",
      "error" :print(e)
    }
  return employees

@app.route('/jobs', methods=["DELETE"])
def deletejobs():
  or_data = request.get_json()
  or_data["table"] = "job"
  try:
    dup_data = {"table": "job"}
    dup_data["id"] = or_data["id"]
    if data_provider.check_duplicate(dup_data):
      employees = data_provider.delete(or_data)
    else:
      return {
        "ERROR 404": "nothing to delete"
      } 
  except Exception as e:
    return {
      "CHECK ":"DOCUMENTATION",
      "error" :print(e)
    }
  return employees

@app.route('/hours', methods=["DELETE"])
def deletehours():
  or_data = request.get_json()
  or_data["table"] = "hours"
  try:
    dup_data = {"table": "hours"}
    dup_data["id"] = or_data["id"]
    if data_provider.check_duplicate(dup_data):
      employees = data_provider.delete(or_data)
    else:
      return {
        "ERROR 404": "nothing to delete"
      } 
  except Exception as e:
    return {
      "CHECK ":"DOCUMENTATION",
      "error" :print(e)
    }
  return employees

@app.route('/wages', methods=["DELETE"])
def deletewages():
  or_data = request.get_json()
  or_data["table"] = "wages"
  try:
    dup_data = {"table": "wages"}
    dup_data["id"] = or_data["id"]
    if data_provider.check_duplicate(dup_data):
      employees = data_provider.delete(or_data)
    else:
      return {
        "ERROR 404": "nothing to delete"
      } 
  except Exception as e:
    return {
      "CHECK ":"DOCUMENTATION",
      "error" :print(e)
    }
  return employees

