from pymock import PyMock

from Services.invite_service import InviteService
from Test.Invite.InviteMockRepository import InviteMockRepository


def inject_mock_invite_service_and_repo(f):
    def decorated_function(*args, **kwargs):
        repo = PyMock.create(InviteMockRepository)
        service = InviteService(repo)
        return f(repo, service, *args, **kwargs)

    return decorated_function


@inject_mock_invite_service_and_repo
def test_invite_valid(repo, service):
    args = ["vkrivozubov", "sokolcom", 105]
    expect_repo_return = {"status": "OK"}
    PyMock.setup(repo.inviteUser(*args)).returns((expect_repo_return, False))

    response, code = service.send_invite(*args)

    assert code == 200
    assert response == '{"status": "OK"}'


@inject_mock_invite_service_and_repo
def test_invite_to_invalid_wardrobe(repo, service):
    args = ["vkrivozubov", "sokolcom", 105]
    expect_repo_return = {"status": "error", "reason": "no such user or wardrobe"}
    PyMock.setup(repo.inviteUser(*args)).returns((expect_repo_return, True))

    response, code = service.send_invite(*args)

    assert code == 405
    assert response == '{"status": "error", "reason": "no such user or wardrobe"}'


@inject_mock_invite_service_and_repo
def test_who_invites_me_valid(repo, service):
    repo_return = [
        {
            'login_that_invites': 'sokolcom',
            'wardrobe_name': 'gucci flip flops',
            'image_url': None
        },
    ]
    PyMock.setup(repo.get_invites_by_login('vkrivozubov')).returns(repo_return)

    response, code = service.who_invites_me('vkrivozubov')

    assert code == 200
    assert response == '[{"login_that_invites": "sokolcom", "wardrobe_name": "gucci flip flops", "image_url": null}]'


@inject_mock_invite_service_and_repo
def test_accept_invite(repo, service):
    args = [1, True]
    PyMock.setup(repo.handleInvite(*args)).returns("OK")

    response, code = service.handle_invite(1, True)

    assert code == 200
    assert response == 'OK'


@inject_mock_invite_service_and_repo
def test_decline_invite(repo, service):
    args = [1, False]
    PyMock.setup(repo.handleInvite(*args)).returns("OK")

    response, code = service.handle_invite(1, True)

    assert code == 200
    assert response == 'OK'
