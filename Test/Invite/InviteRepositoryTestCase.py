from Repositories.InviteRepository import InviteRepository
from Repositories.UserRepository import UserRepository
from Repositories.WardrobeRepository import WardrobeRepository
from Test.Builders.UserBuilder import UserBuilder
from Test.Builders.WardrobeBuilder import WardrobeBuilder
from Test.DatabaseCleaner import DatabaseCleaner
from config import test_db_filename

DB_NAME = test_db_filename

def clean_database(f):
    def decorated_function(*args, **kwargs):
        DatabaseCleaner(DB_NAME).clean()
        return f(*args, **kwargs)

    return decorated_function


def register_vlad(f):
    def decorated_function(*args, **kwargs):
        user_repo = UserRepository(DB_NAME, False)
        builder = UserBuilder()
        builder.with_name("Vlad Krivozubov").with_login("vkrivozubov").with_password("12345678")
        user_repo.register_user(*builder.build_register_data())
        return f(*args, **kwargs)

    return decorated_function


def register_efim(f):
    def decorated_function(*args, **kwargs):
        user_repo = UserRepository(DB_NAME, False)
        builder = UserBuilder().with_name("Efim Sokolov").with_login("sokolcom").with_password("12345678")
        user_repo.register_user(*builder.build_register_data())
        return f(*args, **kwargs)

    return decorated_function

@clean_database
@register_vlad
@register_efim
def test_correct_invite():
    invite_repo = InviteRepository(DB_NAME, False)
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    wardrobe_builder = WardrobeBuilder().with_name("gucci flip flops").with_creator_login('vkrivozubov').with_description('A')

    _, id = wardrobe_repo.create_wardrobe(*wardrobe_builder.build_create_data())
    result, error = invite_repo.inviteUser('vkrivozubov', 'sokolcom', id)

    assert error is False
    assert result == {'status': "OK"}

@clean_database
@register_vlad
def test_incorrect_invite():
    invite_repo = InviteRepository(DB_NAME, False)

    vlados_builder = UserBuilder().with_name("Vlad Krivozubov").with_login("vkrivozubov").with_password("12345678")

    expect = {"status": "error", "reason": "no such user or wardrobe"}


    response, error = invite_repo.inviteUser("this user does not exits", vlados_builder.login, 123)

    assert error
    assert response == expect

@clean_database
@register_vlad
@register_efim
def test_no_such_wardrobe():
    invite_repo = InviteRepository(DB_NAME, False)
    wardrobe_repo = WardrobeRepository(DB_NAME, False)

    wardrobe_builder = WardrobeBuilder() \
        .with_name("gucci flip flops").with_creator_login('vkrivozubov').with_description("No comment")

    expect = {"status": "error", "reason": "no such user or wardrobe"}


    _, id = wardrobe_repo.create_wardrobe(*wardrobe_builder.build_create_data())

    response, error = invite_repo.inviteUser('vkrivozubov', 'sokolcom', id + 5)

    assert error
    assert response == expect


@clean_database
@register_vlad
@register_efim
def test_corrent_get_invites():
    invite_repo = InviteRepository(DB_NAME, False)
    wardrobe_repo = WardrobeRepository(DB_NAME, False)

    wardrobe_builder = WardrobeBuilder() \
        .with_name("gucci flip flops").with_creator_login('vkrivozubov').with_description("No comment")
    _, id = wardrobe_repo.create_wardrobe(*wardrobe_builder.build_create_data())
    invite_repo.inviteUser('vkrivozubov', 'sokolcom', id)

    expect = [{'invite_id': 1, 'login_that_invites': 'vkrivozubov', 'wardrobe_name': 'gucci flip flops', 'image_url': None}]
    response = invite_repo.get_invites_by_login('sokolcom')

    assert response == expect

@clean_database
@register_vlad
def test_empty_invites():
    invite_repo = InviteRepository(DB_NAME, False)

    expect = []
    response = invite_repo.get_invites_by_login('vkrivozubov')

    assert response == expect