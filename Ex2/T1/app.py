from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
api = Api(app)

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


class ProductCollection(Resource):
    def post(self):          
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
        except KeyError:
            return "Incomplete request - missing fields", 400
        except ValueError:
            return "Weight and price must be numbers", 400
        except IntegrityError:
            return "Handle already exists", 409

    def get(self):

        products = Product.query.all()

        product_list = []
        for product in products:
            product_list.append({
                "handle": product.handle,
                "weight": product.weight,
                "price": product.price,
            })

        return product_list, 200


api.add_resource(ProductCollection, "/api/products/")
