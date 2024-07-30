import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import MagicMock
from api.models import db
from api.blueprints.products import products_blueprint

@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(products_blueprint, url_prefix='/products')
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

def test_get_all_products(client: FlaskClient, mocker):
    mock_data = [
        {
            'ProductID': 1,
            'ProductName': 'Product 1',
            'ProductPhotoURL': 'http://example.com/photo1.jpg',
            'ProductStatus': 'Active'
        },
        {
            'ProductID': 2,
            'ProductName': 'Product 2',
            'ProductPhotoURL': 'http://example.com/photo2.jpg',
            'ProductStatus': 'Active'
        }
    ]

    mock_cursor = MagicMock()
    mock_cursor.description = [('id',), ('name',), ('description',), ('price',), ('ProductStatus',)]
    mock_cursor.fetchall.return_value = [tuple(product.values()) for product in mock_data]

    mocker.patch.object(db, 'execute_sql', return_value=mock_cursor)
    mocker.patch('api.schemas.ProductSchema.dump', return_value=mock_data)

    response = client.get('/products/')

    assert response.status_code == 200
    assert response.json['data'] == mock_data
    assert response.json['message'] == ''

def test_get_all_products_error(client: FlaskClient, mocker):
    mocker.patch.object(db, 'execute_sql', side_effect=Exception('Database error'))

    response = client.get('/products/')

    assert response.status_code == 500
    assert response.json['data'] == []
    assert response.json['message'] == 'Database error'