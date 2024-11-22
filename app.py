from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from db_password import my_password
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@127.0.0.1/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models ---------------------------------------------------------------------
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(15))
    orders = db.relationship('Order', backref='customer')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

class CustomerAccount(db.Model):
    __tablename__ = 'customer_accounts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    customer = db.relationship('Customer', backref='customer_account', uselist=False)

order_product_association = db.Table('order_product_association',
                         db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key = True),
                         db.Column('product_id', db.Integer, db.ForeignKey('product_catalog.id'), primary_key = True))

class ProductCatalog(db.Model):
    __tablename__ = 'product_catalog'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    orders = db.relationship('Order', secondary=order_product_association, backref=db.backref('product_catalog'))

# Schemas -------------------------------------------------------------------
class CustomerSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.String()
    phone = fields.String()

    class Meta:
        fields = ('id', 'name', 'email', 'phone')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Customer Routes -------------------------------------------------------------------
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as Err:
        return jsonify(Err.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'Message': 'New customer has been added successfully.'}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify(customers_schema.dump(customers)), 200

# Run Program --------------------------------------------------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
