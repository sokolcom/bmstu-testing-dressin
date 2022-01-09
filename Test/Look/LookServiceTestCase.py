from pymock import PyMock

from Services.look_service import LookService
from Test.Look.LookMockRepository import LookMockRepository


def inject_mock_look_service_and_repo(f):
    def decorated_function(*args, **kwargs):
        repo = PyMock.create(LookMockRepository)
        service = LookService(repo)
        return f(repo, service, *args, **kwargs)

    return decorated_function


@inject_mock_look_service_and_repo
def test_create_look(repo, service):
    args = [(1, 2, 3), "test_look", 1, None]
    PyMock.setup(repo.create_look(*args)).returns({'look_id': 0})

    response, code = service.create_look(*args)

    assert response == '{"look_id": 0}'
    assert code == 200


@inject_mock_look_service_and_repo
def test_update_look(repo, service):
    args = [0, "new_name", None]
    PyMock.setup(repo.update_look(*args)).returns("OK")

    response, code = service.change_look(*args)

    assert response == '{"status": "OK"}'
    assert code == 200


@inject_mock_look_service_and_repo
def test_get_look(repo, service):
    args = [0]
    PyMock.setup(repo.get_look_by_id(*args)).returns({'look_id': 0, 'look_name': 'test_look', 'image': None})

    response, code = service.get_look_by_id(*args)

    assert response == '{"look_id": 0, "look_name": "test_look", "image": null}'
    assert code == 200


@inject_mock_look_service_and_repo
def test_get_look_wrong_id(repo, service):
    args = [0]
    PyMock.setup(repo.get_look_by_id(*args)).returns(None)

    response, code = service.get_look_by_id(*args)

    assert response == '{}'
    assert code == 500
