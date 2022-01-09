from flask import Blueprint
from flask import request

from Repositories.ImageRepository import ImageRepository
from Repositories.UserRepository import UserRepository
from Routers.decorators import validate_api_key
from Services.user_service import UserService

auth_service = Blueprint('auth_service', __name__)
user_service = UserService(UserRepository(), ImageRepository())


@auth_service.route('/login')
@validate_api_key
def login():
    login = request.args.get('login')
    password = request.args.get('password')
    return user_service.login(login, password)


@auth_service.route('/changeAvatar', methods=['POST'])
@validate_api_key
def change_avatar():
    login = request.form.get('login')
    image = request.files['file'].read()
    return user_service.change_avatar(login, image)


@auth_service.route('/changeName', methods=['POST'])
@validate_api_key
def change_name():
    login = request.form.get('login')
    name = request.form.get('new_name')
    return user_service.change_name(login, name)


@auth_service.route('/changePassword', methods=['POST'])
@validate_api_key
def change_password():
    try:
        base = UserRepository()
        if base.is_key_valid(request.form.get('apikey')):
            login = request.form.get('login')
            password = request.form.get('new_password')
            result = base.change_password(login, password)
            respcode = 200 if result else 404
            return result, respcode
        else:
            return 'Key unvalid', 500
    except Exception:
        return "Error", 500


@auth_service.route('/changeLoginTimeBomb', methods=['POST'])
@validate_api_key
def change_login():
    last_login = request.form.get('last_login')
    new_login = request.form.get('new_login')
    return user_service.change_login(last_login, new_login)


@auth_service.route('/register', methods=['POST'])
@validate_api_key
def register():
    login = request.form.get("login")
    username = request.form.get("username")
    password = request.form.get("password")
    try:
        image = request.files['file'].read()
    except Exception:
        image = None
    finally:
        response = user_service.register(login, username, password, image)
        return response
