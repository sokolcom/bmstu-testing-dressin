from flask import Blueprint
from flask import request

from Repositories.ImageRepository import ImageRepository

image_service = Blueprint('image_service', __name__)


@image_service.route('/send', methods=['GET', 'POST'])
def send():
    base = ImageRepository()
    if base.is_key_valid(request.args.get('apikey')):
        try:
            data = request.data
            print(type(data))
            print("Connected to db")
            result = base.save_photo(data)
            print("Everything is fine")
            return result
        except Exception:
            print("Error occured")
            return "ERROR"
    else:
        return 'Key unvalid'


@image_service.route('/getImage', methods=['GET'])
def getImage():
    base = ImageRepository()
    if base.is_key_valid(request.args.get('apikey')):
        try:
            id = request.args.get('id')
            result = base.get_photo(id)
            return result
        except Exception:
            print("Error occured")
            return "ERROR"
    else:
        return 'Key unvalid'


@image_service.route('/changeImage', methods=['POST'])
def changeImage():
    try:
        base = ImageRepository()
        apikey = request.form.get("apikey")
        if base.is_key_valid(apikey):
            id = request.form.get("image_id")
            image = request.files['file'].read()
            base.update_photo(id, image)
            return 'OK', 200
        else:
            return 'Key unvalid', 500
    except Exception:
        return "Error", 500
