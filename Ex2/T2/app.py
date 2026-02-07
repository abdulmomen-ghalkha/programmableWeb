from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound, abort
from werkzeug.routing import BaseConverter

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

class ProductConverter(BaseConverter):
    def to_python(self, handle):
        db_product = Product.query.filter_by(handle=handle).first()
        if db_product is None:
            raise NotFound
        return db_product
    
    def to_url(self, product):
        return product.handle
    


class ProductCollection(Resource):
    def post(self):
    
        try:
            product_name = request.json["handle"]
            product_weight = float(request.json["weight"])
            product_price = float(request.json["price"])
            product = Product(
                handle=product_name,
                weight=product_weight,
                price=product_price
            )
            db.session.add(product)
            db.session.commit()
            return Response(status=201, headers={
                "Location": api.url_for(ProductItem, product=product)
            })
        except KeyError:
            abort(400)
        except ValueError:
            abort(400)
        except IntegrityError:
            abort(409)

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


class ProductItem(Resource):
    def get(self, handle):
        return Response(status=501)





app.url_map.converters["product"] = ProductConverter

api.add_resource(ProductCollection, "/api/products/")
api.add_resource(ProductItem, "/api/products/<product:product>/")


ctx = app.app_context()
ctx.push()
db.create_all()
ctx.pop()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

