from pymock import PyMock

from Services.user_service import UserService
from Test.MockImageRepository import MockImageRepository
from Test.User.UserMockRepository import UserMockRepository


def inject_mock_user_service_and_repo(f):
    def decorated_function(*args, **kwargs):
        repo = PyMock.create(UserMockRepository)
        service = UserService(repo, MockImageRepository())
        return f(repo, service, *args, **kwargs)

    return decorated_function


@inject_mock_user_service_and_repo
def test_register_valid(repo, service):
    args = ['vkrivozubov', 'Vlad Krivozubov', '12345678', None]
    expect_return = {"login": "vkrivozubov", "name": "Vlad Krivozubov", "password": "12345678", "imageid": None}, False
    PyMock.setup(repo.register_user(*args)).returns(expect_return)

    response, code = service.register('vkrivozubov', 'Vlad Krivozubov', '12345678', None)
    assert response == '{"login": "vkrivozubov", "name": "Vlad Krivozubov", "password": "12345678", "imageid": null}'
    assert code == 200


@inject_mock_user_service_and_repo
def test_register_invalid(repo, service):
    args = ['vkrivozubov', 'Vlad Krivozubov', '12345678', None]
    expect_repo_return = ({"status": "Error", "reason": "User already exists"}, True)
    PyMock.setup(repo.register_user(*args)).returns(expect_repo_return)

    response, code = service.register('vkrivozubov', 'Vlad Krivozubov', '12345678', None)
    assert code == 405


@inject_mock_user_service_and_repo
def test_login(repo, service):
    args = ['vkrivozubov', '12345678']
    expect_repo_response = {"login": "vkrivozubov", "name": "Vlad Krivozubov", "password": "12345678", "imageid": None}

    PyMock.setup(repo.get_user_info(*args)).returns(expect_repo_response)

    response, code = service.login(*args)
    assert code == 200


@inject_mock_user_service_and_repo
def test_change_domain_name(repo, service):
    args = ['vkrivozubov', 'God mother']

    PyMock.setup(repo.user_change_name(*args)).returns("OK")

    assert service.change_name(*args) == ('{"status": "OK"}', 200)
