from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from db_password import my_password
from marshmallow import fields, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{my_password}@127.0.0.1/e_commerce_db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Models --------------------------------------------------------------------- Models
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

order_product_association = db.Table(
    'order_product_association',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id', ondelete='CASCADE'), primary_key = True),
    db.Column('product_id', db.Integer, db.ForeignKey('product_catalog.id', ondelete='CASCADE'), primary_key = True))

class ProductCatalog(db.Model):
    __tablename__ = 'product_catalog'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    inventory = db.Column(db.Integer, nullable=False, default=0)
    orders = db.relationship(
        'Order', 
        secondary=order_product_association, 
        backref=db.backref('product_catalog'))

# Schemas ----------------------------------------------------------------------------- Schemas
class CustomerSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.String()
    phone = fields.String()

    class Meta:
        fields = ('id', 'name', 'email', 'phone')

class CustomerAccountSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    password = fields.String()
    customer_id = fields.Integer()

    class Meta:
        fields = ('id', 'username', 'password', 'customer_id')

class ProductCatalogSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
    inventory = fields.Integer(required=True)

    class Meta:
        fields = ('id', 'name', 'price', 'inventory')

class OrderSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    customer_id = fields.Integer(required=True)

    class Meta:
        fields = ('id', 'date', 'customer_id')

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

account_schema = CustomerAccountSchema()
accounts_schema = CustomerAccountSchema(many=True)

product_schema = ProductCatalogSchema()
products_schema = ProductCatalogSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Customer Routes ----------------------------------------------------------------Customer Routes
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as Err:
        return jsonify(Err.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.flush()

    name_split = new_customer.name.split()
    first_initial = name_split[0][0] if len(name_split) > 0 else ""
    second_initial = name_split[1][0] if len(name_split) > 1 else ""
    first_name = name_split[0]

    username = new_customer.name.replace(" ", "").lower()
    username = f'{first_name.lower()}{second_initial.lower()}'
    password = f'{first_initial}{second_initial}{new_customer.id}'
    
    new_account = CustomerAccount(
        username=username,
        password=password,
        customer_id=new_customer.id
        )
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'Message': 'New customer and account have been added successfully.'}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify(customers_schema.dump(customers)), 200

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer_by_id(id):
    customer = Customer.query.filter_by(id=id).first()
    if not customer:
        return jsonify({'Error': f'Customer with ID {id} not found.'}), 404
    return jsonify(customer_schema.dump(customer)), 200

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as Err:
        return jsonify(Err.messages), 400
    
    customer.name = customer_data['name']
    customer.email = customer_data['email']
    customer.phone = customer_data['phone']
    db.session.commit()
    return jsonify({'Message': 'Customer details updated successfully.'}), 200

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'Message': f'Member with ID {id} was deleted successfully.'}), 200

# Customer Account Routes ---------------------------------------------------------Customer Account Routes
@app.route('/customer_accounts', methods=['POST'])
def add_account():
    try:
        account_data = account_schema.load(request.json)
    except ValidationError as Err:
        return jsonify(Err.messages), 400
    
    new_account = CustomerAccount(
        username=account_data['username'], 
        password=account_data['password'], 
        customer_id=account_data['customer_id']
        )
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'Message': 'New account has been added successfully.'}), 201

@app.route('/customer_accounts', methods=['GET'])
def get_accounts():
    accounts = CustomerAccount.query.all()
    return jsonify(accounts_schema.dump(accounts)), 200

@app.route('/customer_accounts/<int:id>', methods=['GET'])
def get_account_by_id(id):
    account = CustomerAccount.query.filter_by(id=id).first()
    if not account:
        return jsonify({'Error': f'Account with ID {id} not found.'}), 404
    return jsonify(account_schema.dump(account)), 200

@app.route('/customer_accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = CustomerAccount.query.get_or_404(id)
    try:
        account_data = account_schema.load(request.json)
    except ValidationError as Err:
        return jsonify(Err.messages), 400
    
    account.username = account_data['username']
    account.password = account_data['password']
    account.customer_id = account_data['customer_id']
    db.session.commit()
    return jsonify({'Message': 'Customer details updated successfully.'}), 200

@app.route('/customer_accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = CustomerAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'Message': f'Account with ID {id} was deleted successfully.'}), 200

# Product Routes ----------------------------------------------------------------------Product Routes
@app.route('/product_catalog', methods=['POST'])
def add_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as Err:
        return jsonify(Err.messages), 400
    
    existing_product = ProductCatalog.query.filter_by(name=product_data['name']).first()
    if existing_product:
        existing_product.inventory += product_data['inventory']
        db.session.commit()
        return jsonify({'Message': f'Product "{existing_product.name}" inventory updated successfully.'}), 200
    else:
        new_product = ProductCatalog(
            name=product_data['name'], 
            price=product_data['price'],
            inventory=product_data['inventory']
            )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'Message': 'New product has been added successfully.'}), 201

@app.route('/product_catalog', methods=['GET'])
def get_products():
    products = ProductCatalog.query.all()
    return jsonify(products_schema.dump(products)), 200

@app.route('/product_catalog/<int:id>', methods=['GET'])
def get_product_by_id(id):
    product = ProductCatalog.query.filter_by(id=id).first()
    if not product:
        return jsonify({'Error': f'Product with ID {id} not found.'}), 404
    return jsonify(product_schema.dump(product)), 200

@app.route('/product_catalog/<int:id>', methods=['PUT'])
def update_product(id):
    product = ProductCatalog.query.get_or_404(id)
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as Err:
        return jsonify(Err.messages), 400
    
    product.name = product_data['name']
    product.price = product_data['price']
    product.inventory = product_data['inventory']
    db.session.commit()
    return jsonify({'Message': 'Product details updated successfully.'}), 200

@app.route('/product_catalog/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = ProductCatalog.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'Message': f'Product with ID {id} was deleted successfully.'}), 200

# Order Routes -----------------------------------------------------------------------------Order Routes
@app.route('/orders', methods=['POST'])
def add_order():
    try:
        order_data = request.json
        customer_id = order_data['customer_id']
        products = order_data['products']
    except KeyError as e:
        return jsonify({'Error': f'Missing key: {str(e)}'}), 400

    new_order = Order(date=order_data['date'], customer_id=customer_id)
    db.session.add(new_order)
    db.session.flush()

    for product_info in products:
        product = ProductCatalog.query.get(product_info['product_id'])
        if not product:
            return jsonify({'Error': f'Product with ID {product_info["product_id"]} not found.'}), 404

        if product.inventory < product_info['quantity']:
            return jsonify({'Error': f'Insufficient inventory for product {product.name}.'}), 400

        product.inventory -= product_info['quantity']
        db.session.add(product)

        db.session.execute(order_product_association.insert().values(
            order_id=new_order.id,
            product_id=product.id
        ))

    db.session.commit()
    return jsonify({'Message': 'Order placed successfully.'}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    order_data = []
    for order in orders:
        order_info = {
            'id': order.id,
            'date': order.date,
            'customer_id': order.customer_id,
            'products': [{'name': p.name, 'quantity': p.inventory} for p in order.product_catalog]
        }
        order_data.append(order_info)
    return jsonify(order_data), 200


# Run Program --------------------------------------------------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
