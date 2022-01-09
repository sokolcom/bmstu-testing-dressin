from pymock import PyMock

from Services.item_service import ItemService
from Test.Item.ItemMockRepository import ItemMockRepository
from Test.MockImageRepository import MockImageRepository


def inject_mock_item_service_and_repo(f):
    def decorated_function(*args, **kwargs):
        repo = PyMock.create(ItemMockRepository)
        service = ItemService(repo, MockImageRepository())
        return f(repo, service, *args, **kwargs)

    return decorated_function


@inject_mock_item_service_and_repo
def test_add_item(repo, service):
    args = ["sokolcom", "some_name", "T-shirt", None]
    repo_return = {'item_id': 0}
    PyMock.setup(repo.add_item(*args)).returns(repo_return)

    response, code = service.add_item("some_name", "sokolcom", "T-shirt", None)
    assert response == '{"item_id": 0}'
    assert code == 200


@inject_mock_item_service_and_repo
def test_update_item(repo, service):
    args = [0, "new_name", None]
    repo_return = "OK"
    PyMock.setup(repo.update_item(*args)).returns(repo_return)

    response, code = service.update_item(*args)

    assert response == '{"status": "OK"}'
    assert code == 200


@inject_mock_item_service_and_repo
def test_update_worng_id_item(repo, service):
    args = [0, "new_name", None]
    repo_return = None
    PyMock.setup(repo.update_item(*args)).returns(repo_return)

    response, code = service.update_item(*args)
    assert response == '{"status": null}'
    assert code == 500


@inject_mock_item_service_and_repo
def test_remove_by_id_item(repo, service):
    args = [0]
    repo_return = "OK"
    PyMock.setup(repo.remove_item(*args)).returns(repo_return)

    response, code = service.remove_item(*args)

    assert response == '{"status": "OK"}'
    assert code == 200


@inject_mock_item_service_and_repo
def test_remove_by_wrong_id_item(repo, service):
    args = [0]
    repo_return = None
    PyMock.setup(repo.remove_item(*args)).returns(repo_return)

    response, code = service.remove_item(*args)

    assert response == '{"status": null}'
    assert code == 500


@inject_mock_item_service_and_repo
def test_get_item_by_id(repo, service):
    args = [0]
    repo_return = {"clothes_id": 0, "clothes_name": "some_name", "type": "T-shirt", "image_id": None,
                   "owner_login": "sokolcom", "image_url": None}
    PyMock.setup(repo.get_item_by_id(*args)).returns(repo_return)

    response, code = service.get_item_by_id(*args)

    assert response == '{"clothes_id": 0, "clothes_name": "some_name", "type": "T-shirt", "image_id": null, "owner_login": "sokolcom", "image_url": null}'
    assert code == 200


@inject_mock_item_service_and_repo
def test_get_item_by_wrong_id(repo, service):
    args = [0]
    repo_return = None

    PyMock.setup(repo.get_item_by_id(*args)).returns(repo_return)

    response, code = service.get_item_by_id(*args)
    
    assert response == '{}'
    assert code == 500
