from pymongo import MongoClient

class MongoDataProvider:
    def __init__(self, host, db, user=None, pwd=None):
        if user and pwd:
            self.client = MongoClient(f"mongodb://{user}:{pwd}@{host}/{db}")
        else:
            self.client = MongoClient(f"mongodb://{host}/{db}")
        self.db = self.client["Company"]

    def check_duplicate(self, or_data) -> bool:
      table = or_data["table"]
      del or_data["table"]
      if not table:
          raise ValueError("No table specified in query")
      collection = self.db[table]
      if len(or_data)>0:
          documents=list(collection.find(or_data))
      else:
          documents=list(collection.find())
      for document in documents:
        document["_id"] = str(document["_id"])
      # if document["id"]==or_data["id"]:  
      return len(documents) !=0

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

    def get(self, query):
        collection_name = query["table"]
        del query["table"]
        if not collection_name:
            raise ValueError("No table specified in query")
        collection = self.db[collection_name]
        if len(query)>0:
            documents=list(collection.find(query))
        else:
            documents=list(collection.find())
        for document in documents:
          document["_id"] = str(document["_id"])
        return documents
    
    def post(self, or_data):
        table = or_data.get("table")
        if not table:
            raise ValueError("No table specified in query")
        del or_data["table"]
        collection = self.db[table]
        result = collection.insert_one(or_data)
        document = or_data.copy()
        document["_id"] = str(result.inserted_id)
        return document

    def put(self, or_data):
        table = or_data.get("table")
        del or_data["table"]
        if not table:
            raise ValueError("No table specified in query")
        filter_data = {}
        update_data = {}
        filter_data["filter"]={"id": or_data["id"]}
        for k in or_data:
            update_data["update"]={k: or_data[k]}
        print(filter_data["filter"])
        print(update_data["update"])
        collection = self.db[table]
        result = collection.update_one(filter_data["filter"], {"$set": update_data["update"]})
        return {
          "status_code": 200,
          "message": "Updated"
        }

    def delete(self,or_data):
        table = or_data.get("table")
        if not table:
            raise ValueError("No table specified in query")
        del or_data["table"]
        collection = self.db[table]
        result = collection.delete_one(or_data)
        document = or_data.copy()
        return {
           "Status_code":200,
           "message" : "Deleted"
        }
       
    def cal_salary_from_hours(self, hours, emp_id):
        wages = self.get({
        "table": "wages",
        "employee_id": emp_id
        })
        print("Fetched hours data:", wages)

        if wages:
            # hours_worked = hours[0][2]
            hourly_wage = wages[0]["hourly_wage"]
            print("Hours worked:", hourly_wage)

            time = int(hourly_wage)
            base_salary = time * hours
            self.store_salary(base_salary, emp_id)  

    def cal_salary_from_wages(self, wages, emp_id):
        hours = self.get({
        "table": "hours",
        "employee_id": emp_id
        })
        print("Fetched hours data:", hours)
        if hours:
            # hours_worked = hours[0][2]
            hours_worked = hours[0]["hours_worked"]
            print("Hours worked:", hours_worked)
            time = int(hours_worked)
            base_salary = time * wages
            self.store_salary(base_salary, emp_id)    