from flask import Blueprint
from flask import request

from Repositories.ImageRepository import ImageRepository
from Repositories.WardrobeRepository import WardrobeRepository
from Routers.decorators import validate_api_key
from Services.wardrobe_service import WardrobeService

wardrobe_router = Blueprint('wardrobe_service', __name__)
service = WardrobeService(WardrobeRepository(), ImageRepository())


@wardrobe_router.route('/getWardrobes')
@validate_api_key
def getWardrobes():
    try:
        login = request.args.get('login')
        return service.get_wardrobes(login)
    except Exception as e:
        print(f'/getWardrobes: {e}')
        return None, 500


@wardrobe_router.route('/getWardrobeById')
@validate_api_key
def getWardrobeById():
    try:
        wardrobe_id = request.args.get('wardrobe_id')
    except Exception as e:
        print(f'/getWardrobeById: {e}')
        return None, 500


@wardrobe_router.route('/createWardrobe', methods=['POST'])
@validate_api_key
def createWardrobe():
    try:
        wardrobe_name = request.form.get("wardrobe_name")
        wardrobe_description = request.form.get("wardrobe_description")
        login = request.form.get("login")
        try:
            image = request.files['file'].read()
        except Exception:
            image = None
        return service.create_wardrobe(login, wardrobe_name, wardrobe_description, image)
    except Exception as e:
        print(f'/createWardrobe: {e}')
        return None, 500


@wardrobe_router.route('/deleteWardrobe')
@validate_api_key
def deleteWardrobe():
    try:
        wardrobe_id = request.args.get('wardrobe_id')
        login = request.args.get('login')
        return service.delete_wardrobe(wardrobe_id, login)
    except Exception as e:
        print(f'/deleteWardrobe: {e}')
        return None, 500


@wardrobe_router.route('/removeUserFromWardrobe')
@validate_api_key
def removeUserFromWardrobe():
    try:
        wardrobe_id = request.args.get('wardrobe_id')
        login = request.args.get('remove_login')
        return service.remove_user_from_wardrobe(wardrobe_id, login)
    except Exception as e:
        print(f'/removeUserFromWardrobe: {e}')
        return None, 500


@wardrobe_router.route('/updateWardrobe', methods=['POST'])
@validate_api_key
def updateWardrobe():
    try:
        wardrobe_id = request.form.get("wardrobe_id")
        new_name = request.form.get("new_name")
        image = request.files['file'].read()
        return service.update_wadrobe(wardrobe_id, new_name, image)
    except Exception as e:
        print(f'/updateWardrobe: {e}')
        return None, 500
