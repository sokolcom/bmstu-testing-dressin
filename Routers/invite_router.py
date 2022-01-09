from flask import Blueprint
from flask import request

import Repositories.InviteRepository as repository
from Routers.decorators import validate_api_key
from Services.invite_service import InviteService

invite_router = Blueprint('invite_service', __name__)
invite_service = InviteService(repository.InviteRepository())


@invite_router.route('/whoInvitesMe')
@validate_api_key
def who_invites_me():
    login = request.args.get('login')
    return invite_service.who_invites_me(login)


@invite_router.route('/sendInvite')
@validate_api_key
def send_invite():
    try:
        my_login = request.args.get('my_login')
        wardrobe_id = int(request.args.get('wardrobe_id'))
        login_to_invite = request.args.get('login_to_invite')
        return invite_service.send_invite(my_login, login_to_invite, wardrobe_id)
    except Exception as e:
        print(f'def send_invite(): {e}')
        return "/sendInvite invalid parameters", 500


@invite_router.route('/getWardrobeUsers')
@validate_api_key
def get_wardrobe_users():
    wardrobe_id = request.args.get('wardrobe_id')
    return invite_service.get_wardrobe_users(wardrobe_id)


@invite_router.route('/handleInvite')
@validate_api_key
def handle_invite():
    try:
        invite_id = int(request.args.get('inviteId'))
        accepted = int(request.args.get('accepted'))
    except Exception:
        accepted = 0
    return invite_service.handle_invite(invite_id, accepted)
