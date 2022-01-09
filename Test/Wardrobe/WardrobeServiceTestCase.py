from pymock import PyMock

from Services.wardrobe_service import WardrobeService
from Test.MockImageRepository import MockImageRepository
from Test.Wardrobe.WardrobeMockRepository import WardrobeMockRepository


def inject_mock_wardrobe_service_and_repo(f):
    def decorated_function(*args, **kwargs):
        repo = PyMock.create(WardrobeMockRepository)
        service = WardrobeService(repo, MockImageRepository())
        return f(repo, service, *args, **kwargs)

    return decorated_function



@inject_mock_wardrobe_service_and_repo
def test_valid_create(repo: WardrobeMockRepository, service: WardrobeService):
    args = ['vkrivozubov', 'w1', 'no desc', None]
    expect = '{"status": "OK"}'

    repo_args = args
    expect_repo_return = ("OK", 1)
    PyMock.setup(repo.create_wardrobe(*repo_args)).returns(expect_repo_return)

    response, code = service.create_wardrobe(*args)

    assert code == 200
    assert response == expect


@inject_mock_wardrobe_service_and_repo
def test_internal_creatoin_error(repo: WardrobeMockRepository, service: WardrobeService):
    args = ['vkrivozubov', 'w1', 'no desc', None]
    expect = '{"status": "error", "reason": "internal server error"}'

    repo_args = args
    expect_repo_return = None
    PyMock.setup(repo.create_wardrobe(*repo_args)).returns(expect_repo_return)

    response, code = service.create_wardrobe(*args)

    assert code == 500
    assert response == expect


@inject_mock_wardrobe_service_and_repo
def test_remove_user_invalid(repo: WardrobeMockRepository, service: WardrobeService):
    args = [5, 'vkrivozubov']
    expect = '{"status": "error", "reason": "Not owner tried to remove owner"}'

    repo_args = args
    expect_repo_return = ({"status": "error", "reason": "Not owner tried to remove owner"}, True)
    PyMock.setup(repo.remove_user_from_wardrobe(*repo_args)).returns(expect_repo_return)

    response, code = service.remove_user_from_wardrobe(*args)

    assert code == 405
    assert response == expect


@inject_mock_wardrobe_service_and_repo
def test_remove_user_valid(repo: WardrobeMockRepository, service: WardrobeService):
    args = [5, 'v']
    expect = '{"status": "OK"}'

    repo_args = args
    expect_repo_return = ({"status": 'OK'}, False)
    PyMock.setup(repo.remove_user_from_wardrobe(*repo_args)).returns(expect_repo_return)

    response, code = service.remove_user_from_wardrobe(*args)

    assert code == 200
    assert response == expect
