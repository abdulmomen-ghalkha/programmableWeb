from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class StorageItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    location = db.Column(db.String(64), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    product = db.relationship("Product", back_populates="in_storage")
    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), nullable=False, unique=True)    
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_storage = db.relationship("StorageItem", back_populates="product")


@app.route("/products/add/", methods=["POST"])
def add_product():
    try:
        product_name = request.json["handle"]
        product = Product.query.filter_by(handle=product_name).first()
        if product is None:
            product_weight = float(request.json["weight"])
            product_price = float(request.json["price"])
            product = Product(
                handle=product_name,
                weight=product_weight,
                price=product_price
            )
            db.session.add(product)
            db.session.commit()
            return "Product added", 201
        else:
            return "Handle already exists", 409
    except KeyError:
        return "Incomplete request - missing fields", 400
    except ValueError:
        return "Weight and price must be numbers", 400
    except BadRequest:
        return "Request content type must be JSON", 415


@app.route("/storage/<product_name>/add/", methods=["POST"])
def add_storage(product_name):
    try:
        product_name = Product.query.filter_by(handle=product_name).first()
        if product_name:
            data = request.get_json()
            product_qty = int(data["qty"])
            product_location = data["location"]
            storage_item = StorageItem(
                location=product_location,
                qty=product_qty,
                product=product_name
            )
            db.session.add(storage_item)
            db.session.commit()
            return "Storage updated succefully", 201
        else:
            return "Product not found", 404
    except KeyError:
        return "Incomplete request - missing fields", 400
    except ValueError:
        return "Qty must be an integer", 400
    except BadRequest:
        return "Request content type must be JSON", 415


@app.route("/storage/", methods=["GET"])
def get_inventory():
    if request.method != "GET":
        return "GET method required", 405

    products = Product.query.all()

    inventory_list = []
    for product in products:
        inventory_list.append({
            "handle": product.handle,
            "weight": product.weight,
            "price": product.price,
            "inventory": [
                [item.location, item.qty]
                for item in product.in_storage
            ]
        })

    return jsonify(inventory_list), 200
