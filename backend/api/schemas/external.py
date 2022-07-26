from marshmallow import Schema, fields, validate


class Inventory(Schema):
    article_id = fields.String(data_key="art_id")
    name = fields.String()
    stock = fields.Number()


class ContainArticles(Schema):
    article_id = fields.String(data_key="art_id")
    amount = fields.Number(data_key="amount_of")


class Product(Schema):
    name = fields.String()
    contain_articles = fields.List(fields.Nested(ContainArticles()))


class ImportFile(Schema):
    inventory = fields.List(fields.Nested(Inventory()), required=False)
    products = fields.List(fields.Nested(Product()), required=False)


class MessageResponse(Schema):
    message = fields.String()


class Sale(Schema):
    amount = fields.Integer(validate=validate.Range(min=1, max=999))


class ProductStock(Schema):
    product_id = fields.String()
    name = fields.String()
    stock = fields.Integer()


class ProductsResponse(Schema):
    products = fields.List(fields.Nested(ProductStock()))
