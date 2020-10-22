import datetime
from shop import db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.DateTime)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    delete_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_order = db.relationship('Orders', backref='user_order', lazy='select')
    user_cart = db.relationship('Cart', backref='user_cart', lazy='select')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(20))
    role_user = db.relationship('Users', backref='role_user', lazy='select')


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(40), nullable=False)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer, nullable=False)
    product_description = db.Column(db.String(500), nullable=False)
    image_product = db.Column(db.String(500), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    delete_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    product_order_detail = db.relationship('Order_detail', backref='product_order_detail',
                                           lazy='select')
    product_warehouse = db.relationship('Warehouse', backref='product_warehouse',
                                        lazy='select')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(40))
    category_product = db.relationship('Products', backref='category_product',
                                       lazy='select')
    category_warehouse = db.relationship('Warehouse', backref='category_warehouse',
                                         lazy='select')


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Order_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    delete_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    order_order_details = db.relationship('Order_detail', backref='order_order_details',
                                          lazy='select')
    order_shipper = db.relationship('Shipper', backref='order_shipper',
                                    lazy='select')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Order_detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Integer)
    note = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


class Shipper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipper_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(100))
    ship_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    create_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    delete_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    update_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

db.create_all()