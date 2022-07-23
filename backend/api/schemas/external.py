from marshmallow import Schema, fields


class Inventory(Schema):
    article_id = fields.Number(data_key="art_id")
    name = fields.String()
    stock = fields.Number()


class ContainArticles(Schema):
    article_id = fields.Number(data_key="art_id")
    amount = fields.Number(data_key="amount_of")


class Product(Schema):
    name = fields.String()
    contain_articles = fields.List(fields.Nested(ContainArticles()))


class ImportFile(Schema):
    inventory = fields.List(fields.Nested(Inventory()), required=False)
    products = fields.List(fields.Nested(Product()), required=False)
