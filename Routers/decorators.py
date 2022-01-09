import functools

import flask

from Repositories.BaseDataBase import BaseRepository


def validate_api_key(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        repo = BaseRepository()
        if not repo.is_key_valid(flask.request.args.get('apikey')):
            return 'Key unvalid', 403
        return f(*args, **kwargs)

    return decorated_function
