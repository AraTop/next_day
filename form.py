import json
from flask import Flask , request , jsonify
from flask_sqlalchemy import SQLAlchemy 
from data import ofers , orders , users

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///memory.db"
app.config["JSON_AS_ASCII"] = False
db = SQLAlchemy(app)

class Users(db.Model):
   __tablename__ = "Users"

   id = db.Column(db.Integer, primary_key=True)
   first_name = db.Column(db.String(100))
   last_name = db.Column(db.String(150))
   age = db.Column(db.Integer)
   email = db.Column(db.String(300),unique=True)
   role = db.Column(db.String(100))
   phone = db.Column(db.String(100),unique=True)

   def to_dict(self):
      return {col.name: getattr(self, col.name) for col in self.__table__.columns}
      
class Orders(db.Model):
   __tablename__ = "Orders"

   id = db.Column(db.Integer, primary_key= True)
   name = db.Column(db.String(100))
   description = db.Column(db.String(500))
   start_date = db.Column(db.String(20))
   end_date = db.Column(db.String(20))
   address = db.Column(db.String(20))
   price = db.Column(db.Integer)
   customer_id = db.Column(db.Integer, db.ForeignKey("Orders.id"))
   executor_id = db.Column(db.Integer, db.ForeignKey("Users.id"))

   def to_dict(self):
      return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Offers(db.Model):
   __tablename__ = "Offers"

   id = db.Column(db.Integer, primary_key=True)
   order_id = db.Column(db.Integer, db.ForeignKey("Orders.id"))
   executor_id = db.Column(db.Integer, db.ForeignKey("Users.id"))

   def to_dict(self):
      return {col.name: getattr(self, col.name) for col in self.__table__.columns}

with app.app_context():
   db.drop_all()
   db.create_all()

   for user in users:
      user_new = Users(id=user["id"] , first_name=user["first_name"] ,last_name=user["last_name"] ,
                  age=user["age"] , email=user["email"] , role=user["role"] , phone=user["phone"])

      db.session.add(user_new)
      db.session.commit()

   for order in orders:
      order_new = Orders(id=order["id"] , name=order["name"] ,description=order["description"] ,
                  start_date=order["start_date"] , end_date=order["end_date"] , address=order["address"],
                  price=order["price"], customer_id=order["customer_id"], executor_id=order["executor_id"])

      db.session.add(order_new)
      db.session.commit()

   for offer in ofers:
      offer_new = Offers(id=offer["id"] , order_id=offer["order_id"], executor_id=offer["executor_id"])

      db.session.add(offer_new)
      db.session.commit()

#--------------------------------------------GET-----------------------------------------------------------------------

@app.route("/users")
def users():
   data = Users.query.all()
   output = [usr.to_dict()for usr in data]
   return jsonify(output)

@app.route("/user/<int:number>")
def user(number):
   data = Users.query.get(number)
   output = [data.to_dict()]
   return jsonify(output)

@app.route("/orders")
def orders():
   data = Orders.query.all()
   output = [usr.to_dict()for usr in data]
   return jsonify(output)

@app.route("/order/<int:number>")
def order(number):
   data = Users.query.get(number)
   output = [data.to_dict()]
   return jsonify(output)

@app.route("/offers")
def offers():
   data = Offers.query.all()
   output = [usr.to_dict()for usr in data]
   return jsonify(output)

@app.route("/offer/<int:number>")
def offer(number):
   data = Offers.query.get(number)
   output = [data.to_dict()]
   return jsonify(output)

# users

@app.post("/users")
def users_post():
   data_user = json.loads(request.data)
   output = Users(**data_user)
   db.session.add(output)
   db.session.commit()
   return "yessss", 201

@app.put("/user/<uid>")
def user_put(uid):
   data_user = json.loads(request.data)
   output = Users.query.get(uid)
   
   output.first_name = data_user["first_name"]
   output.last_name = data_user["last_name"]
   output.role = data_user["role"]
   output.phone = data_user["phone"]
   output.email = data_user["email"]
   output.age = data_user["age"]

   db.session.add(output)
   db.session.commit()
   return "yessss", 200

@app.delete("/user/<uid>")
def user_delete(uid):
   user = Users.query.get(uid)
   db.session.delete(user)
   db.session.commit()
   return "yessss", 200

#  orders

@app.post("/orders")
def orders_post():
   data_user = json.loads(request.data)
   output = Orders(**data_user)
   db.session.add(output)
   db.session.commit()
   return "yessss", 201

@app.put("/order/<uid>")
def order_put(uid):
   data_user = json.loads(request.data)
   output = Orders.query.get(uid)
   
   output.name = data_user["name"]
   output.description = data_user["description"]
   output.start_date = data_user["start_date"]
   output.end_date = data_user["end_date"]
   output.address = data_user["address"]
   output.price = data_user["price"]
   output.customer_id = data_user["customer_id"]
   output.executor_id = data_user["executor_id"]

   db.session.add(output)
   db.session.commit()
   return "yessss", 200

@app.delete("/order/<uid>")
def order_delete(uid):
   user = Orders.query.get(uid)
   db.session.delete(user)
   db.session.commit()
   return "yessss", 200

#   offers

@app.post("/offers")
def offers_post():
   data_user = json.loads(request.data)
   output = Offers(**data_user)
   db.session.add(output)
   db.session.commit()
   return "yessss", 201

@app.put("/offer/<uid>")
def offer_put(uid):
   data_user = json.loads(request.data)
   output = Offers.query.get(uid)
   
   output.order_id = data_user["order_id"]
   output.executor_id = data_user["executor_id"]

   db.session.add(output)
   db.session.commit()
   return "yessss", 201

@app.delete("/offer/<uid>")
def offer_delete(uid):
   user = Offers.query.get(uid)
   db.session.delete(user)
   db.session.commit()
   return "yessss", 200


if __name__ == "__main__":
   app.run()