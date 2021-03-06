import prettytable
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datas import data_users, data_orders, offer
from sqlalchemy import Integer, Column, String

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'email': self.email,
            'role': self.role,
            'phone': self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'address': self.address,
            'price': self.price,
            'customer_id': self.customer_id,
            'executor_id': self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'executor_id': self.executor_id
        }


# db.drop_all()
# db.create_all()

users = []
for data_user in data_users:
    user = User(
        id=data_user['id'],
        first_name=data_user['first_name'],
        last_name=data_user['last_name'],
        age=data_user['age'],
        email=data_user['email'],
        role=data_user['role'],
        phone=data_user['phone']
    )
    users.append(user)

orders = []
for data_order in data_orders:
    order = Order(
        id=data_order['id'],
        name=data_order['name'],
        description=data_order['description'],
        start_date=data_order['start_date'],
        end_date=data_order['end_date'],
        address=data_order['address'],
        price=data_order['price'],
        customer_id=data_order['customer_id'],
        executor_id=data_order['executor_id']
    )
    orders.append(order)

offers = []
for off in offer:
    ofer = Offer(id=off['id'], order_id=off['order_id'], executor_id=off['executor_id'])
    offers.append(ofer)


# db.session.add_all(users)
# db.session.add_all(offers)
# db.session.add_all(orders)
# db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def step_3and6():
    if request.method == 'GET':
        users = db.session.query(User).all()
        result = []
        for us in users:
            result.append(us.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        new_user = User(
            id=31,
            first_name='????????????',
            last_name='????????',
            age=35,
            email='ggg12gg@mail.ru',
            role='customer',
            phone='4455664'
        )
        db.session.add(new_user)
        db.session.commit()


@app.route('/users/<int:ind>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def step_3_6_ind(ind: int):
    if request.method == 'GET':
        user = User.query.get(ind)
        result = user.to_dict()
        return jsonify(result)
    elif request.method == 'PUT':
        user = User.query.get(ind)
        user.last_name = '??????????????'
        db.session.add(user)
        db.session.commit()
        return f"???????????????????????? {ind} ????????????????"
    elif request.method == 'DELETE':
        user = User.query.get(ind)
        db.session.delete(user)
        db.session.commit()
        return f"???????????????????????? {ind} ????????????"


@app.route('/orders', methods=['GET', 'POST'])
def step_4and7():
    if request.method == 'GET':
        orders = db.session.query(Order).all()
        result = []
        for ord in orders:
            result.append(ord.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        new_order = Order(
            id=50,
            name='new name',
            description='new description',
            start_date='01/01/2022',
            end_date='11/01/2022',
            address='new address',
            price=100,
            customer_id=5,
            executor_id=10
        )
        db.session.add(new_order)
        db.session.commit()


@app.route('/orders/<int:ind>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def step_4_7_ind(ind: int):
    if request.method == 'GET':
        order_ = Order.query.get(ind)
        result = order_.to_dict()
        return jsonify(result)
    elif request.method == 'PUT':
        order = Order.query.get(ind)
        order.start_date = '12/01/2022'
        db.session.add(order)
        db.session.commit()
        return f"?????????? {ind} ????????????????"
    elif request.method == 'DELETE':
        order = Order.query.get(ind)
        db.session.delete(order)
        db.session.commit()
        return f"?????????? {ind} ????????????"


@app.route('/offers', methods=['GET', 'POST'])
def step_5():
    if request.method == 'GET':
        offers_ = db.session.query(Offer).all()
        result = []
        for offer_ in offers_:
            result.append(offer_.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        new_offer = Order(
            id=70,
            order_id=20,
            executor_id=30
        )
        db.session.add(new_offer)
        db.session.commit()


@app.route('/offers/<int:ind>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def step_5_ind(ind: int):
    if request.method == 'GET':
        offer_ = Offer.query.get(ind)
        result = offer_.to_dict()
        return jsonify(result)
    elif request.method == 'PUT':
        offer = Offer.query.get(ind)
        offer.order_id = 25
        db.session.add(offer)
        db.session.commit()
        return f"?????????????????????? {ind} ??????????????????"
    elif request.method == 'DELETE':
        offer = Offer.query.get(ind)
        db.session.delete(offer)
        db.session.commit()
        return f"?????????????????????? {ind} ??????????????"



if __name__ == '__main__':
    app.run(debug=True)
