from flask import Blueprint, jsonify
from api.models import db
from api.schemas import ProductSchema

products_blueprint = Blueprint('products_blueprint', __name__)

@products_blueprint.route('/', methods=['GET'])
def get_all_products():
   
    try:
        query = "SELECT * FROM Product WHERE ProductStatus = 'Active'"
        cursor = db.execute_sql(query)
        products = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
        product_schema = ProductSchema(many=True)
        products_serialized = product_schema.dump(products)
    except Exception as err:
        return jsonify({'data': [], 'message': str(err)}), 500
    return jsonify({'data': products_serialized, 'message': ''}), 200
