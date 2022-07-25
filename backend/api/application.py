from http import HTTPStatus

from flask import Flask, abort
from flask.views import MethodView
from flask_cors import CORS
from flask_smorest import Api, Blueprint

from api.config.read import CONFIG
from api.schemas.external import MessageResponse, Sale, ProductsResponse
from api.services.products import get_products_stock
from api.services.sales import register_sale, ProductNotFound

blp = Blueprint("products", "products", url_prefix="/products")

INVALID_PRODUCT_MESSAGE = "Invalid Product"


@blp.route("/")
class Products(MethodView):
    @blp.response(200, ProductsResponse)
    def get(self):
        """Get products stock"""
        return dict(products=get_products_stock())


@blp.route("/<product_id>/sale")
class ProductsById(MethodView):
    @blp.arguments(Sale)
    @blp.doc(responses={HTTPStatus.NOT_FOUND: {"description": INVALID_PRODUCT_MESSAGE}})
    @blp.response(201, MessageResponse)
    def post(self, sale_data, product_id):
        """Register a sale of a product"""
        try:
            register_sale(product_id=product_id, amount=sale_data["amount"])
        except ProductNotFound:
            abort(HTTPStatus.NOT_FOUND)
        return dict(message="OK"), HTTPStatus.CREATED


def create_application() -> Flask:
    """Factory function for bootstrapping Flask application"""
    app = Flask(__name__)
    app.config.from_mapping(CONFIG)
    api = Api(app)

    CORS(app)

    @app.route("/health")
    def hello_world():
        return "OK"

    api.register_blueprint(blp)

    return app


if __name__ == "__main__":
    create_application().run(port=5000)
