from flask import Blueprint
from flask import send_file

ios_service = Blueprint('ios_service', __name__)


@ios_service.route('/terms')
def terms():
    return send_file("terms.html")


@ios_service.route('/support')
def support():
    return send_file("support.html")
