from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(120), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productName = db.Column(db.String, nullable=True)
    partNumber = db.Column(db.String, nullable=True)
    productLabel = db.Column(db.String, nullable=True)
    startingInventory = db.Column(db.Integer, nullable=True)
    inventoryIn = db.Column(db.Integer, nullable=True)
    inventoryOut = db.Column(db.Integer, nullable=True)
    inventoryOnHand = db.Column(db.Integer, nullable=True)
    minimumReq = db.Column(db.Integer, nullable=True)
    image = db.Column(db.String(200), nullable=True)
    sale_price = db.Column(db.Float, nullable=False)
    buy_price = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('productName', 'partNumber'),
    )

class Order(db.Model):
    orderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    oDate = db.Column(db.Date, nullable=False)
    totalAmount = db.Column(db.Float, nullable=False)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    cust_name = db.Column(db.String, nullable=False)
    cust_phone = db.Column(db.String, nullable=False)

    user = db.relationship('User', backref='orders', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.orderId'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = db.relationship('Product', backref='order_items')

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    cart_items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    product = db.relationship('Product', backref='cart_items')

class Purchase(db.Model):
    purchaseId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_name = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    part_number = db.Column(db.String, nullable=False)
    numberIn = db.Column(db.Integer, nullable=False)
    pDate = db.Column(db.Date, nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier = db.Column(db.String, nullable=False)
