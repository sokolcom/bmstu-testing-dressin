from flask import Blueprint
from flask import request

import json_routine as js
from Repositories.ImageRepository import ImageRepository
from Repositories.LookRepository import LookRepository
from Services.look_service import LookService
from Routers.decorators import validate_api_key

look_router = Blueprint('look_service', __name__)
look_service = LookService(LookRepository())

@look_router.route('/createLook', methods=['POST'])
@validate_api_key
def createLook():
    try:
        items_ids = js.parseJSONArray(request.form.get("items_ids"))
        look_name = request.form.get("look_name")
        wardrobe_id = request.form.get("wardrobe_id")
        file = request.files['file'].read()
        return look_service.create_look(items_ids, look_name, wardrobe_id, file)
    except Exception as e:
        print(f'/createLook: {e}')
        return None, 500


@look_router.route('/updateLookItems', methods=['POST'])
@validate_api_key
def updateLookItems():
    try:
        base = LookRepository()
        items_ids = js.parseJSONArray(request.form.get("items_ids"))
        look_id = request.form.get("look_id")
        base.update_look_items(look_id, items_ids)
        return 'OK', 200
    except Exception as e:
        print(f'/updateLookItems: {e}')
        return "Error", 500


@look_router.route('/updateLook', methods=['POST'])
@validate_api_key
def updateLook():
    try:
        look_id = request.form.get("look_id")
        new_name = request.form.get("new_name")
        image = request.files['file'].read()
        return look_service.change_look(look_id, new_name, image)
    except Exception as e:
        print(f'/updateLook: {e}')
        return "Error", 500


@look_router.route('/deleteItemFromLook')
@validate_api_key
def deleteItemFromLook():
    try:
        base = LookRepository()
        look_id = request.args.get("look_id")
        item_id = request.args.get("item_id")
        base.remove_item_from_look_by_id(look_id, item_id)
        return 'OK'
    except Exception as e:
        print(f'/deleteItemFromLook: {e}')
        return "Error", 500


@look_router.route('/getLookById')
@validate_api_key
def getLookById():
    try:
        base = LookRepository()
        look_id = request.args.get("look_id")
        response = base.get_look_by_id(look_id)
        respcode = 200 if response and response != '[]' else 500
        return response, respcode
    except Exception as e:
        print(f'/getLookById: {e}')
        return "Error", 500


@look_router.route('/getLookByWardrobe')
@validate_api_key
def getLookByWardrobe():
    try:
        base = LookRepository()
        wardrobe_id = request.args.get("wardrobe_id")
        response = base.get_look_by_wardrobe(wardrobe_id)
        return response
    except Exception as e:
        print(f'/getLookByWardrobe: {e}')
        return "Error", 500


@look_router.route('/removeLook')
@validate_api_key
def removeLook():
    try:
        base = LookRepository()
        look_id = request.args.get("look_id")
        response = base.remove_look(look_id)
        respcode = 200 if response else 500
        return response, respcode
    except Exception as e:
        print(f'/removeLook: {e}')
        return "Error", 500
