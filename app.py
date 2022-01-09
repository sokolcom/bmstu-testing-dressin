from flask import Flask, request, send_file, send_from_directory
from Repositories.ItemRepository import ItemRepository
from Repositories.LookRepository import LookRepository
from Repositories.BaseDataBase import BaseRepository
from Routers.auth_router import auth_service
from Routers.image_router import image_service
from Routers.wardrobe_router import wardrobe_router
from Routers.invite_router import invite_router
from Routers.look_router import look_router
from Routers.item_router import item_router
from Routers.ios_application_service import ios_service

from Routers.decorators import validate_api_key

app = Flask(__name__, static_url_path='')

app.register_blueprint(auth_service)
app.register_blueprint(image_service)
app.register_blueprint(wardrobe_router)
app.register_blueprint(invite_router)
app.register_blueprint(look_router)
app.register_blueprint(item_router)
app.register_blueprint(ios_service)

app.config['UPLOAD_FOLDER'] = '/files'

@app.route('/')
@validate_api_key
def index():
    return "API WORKING GOOD"

@app.route('/getAllItems', methods=['GET'])
def getAllItems():
    base = ItemRepository()
    if base.is_key_valid(request.args.get('apikey')):
        try:
            login = request.args.get('login')
            result = base.get_all_items_by_user(login)
            return result
        except Exception:
            print("Error occured")
            return "ERROR"
    else:
        return 'Key unvalid'

@app.route('/getLook')
def getLook():
    try:
        base = LookRepository()
        if base.is_key_valid(request.args.get('apikey')):
            look_id = request.args.get('look_id')
            result = base.get_look_items(look_id)
            respcode = 200 if result else 404
            return result, respcode
        else:
            return 'Key unvalid'
    except Exception:
        return "Error"



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)







def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData