from flask import Blueprint
from flask import request

from Repositories.ImageRepository import ImageRepository
from Repositories.ItemRepository import ItemRepository
from Routers.decorators import validate_api_key
from Services.item_service import ItemService

item_router = Blueprint('item_service', __name__)
item_service = ItemService(ItemRepository(), ImageRepository())


@item_router.route('/getItemById')
@validate_api_key
def get_item_by_id():
    try:
        item_id = request.args.get('item_id')
        return item_service.get_item_by_id(item_id)
    except Exception as e:
        print(f'/getItemById: {e}')
        return None, 500


@item_router.route('/removeItem')
@validate_api_key
def remove_item():
    try:
        item_id = request.args.get('item_id')
        return item_service.remove_item(item_id)
    except Exception as e:
        print(f'/removeItem: {e}')
        return None, 500


@item_router.route('/addItem', methods=['POST'])
@validate_api_key
def add_item():
    try:
        item_name = request.form.get("new_name")
        login = request.form.get("login")
        item_type = request.form.get("item_type")
        file = request.files['file'].read()
        return item_service.add_item(item_name, login, item_type, file)
    except Exception as e:
        print(f'/addItem: {e}')
        return None, 500


@item_router.route('/updateItem', methods=['POST'])
@validate_api_key
def update_item():
    try:
        item_id = request.form.get("item_id")
        new_name = request.form.get("new_name")
        file = request.files['file'].read()
        return item_service.update_item(item_id, new_name, file)
    except Exception as e:
        print(f'/updateItem: {e}')
        return None, 500
