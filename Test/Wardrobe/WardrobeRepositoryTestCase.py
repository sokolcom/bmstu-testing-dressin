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


def register_erokha(f):
    def decorated_function(*args, **kwargs):
        user_repo = UserRepository(DB_NAME, False)
        builder = UserBuilder()
        builder.with_name("Vlad Krivozubov").with_login("vkrivozubov").with_password("12345678")
        user_repo.register_user(*builder.build_register_data())
        return f(*args, **kwargs)

    return decorated_function


def register_zak(f):
    def decorated_function(*args, **kwargs):
        user_repo = UserRepository(DB_NAME, False)
        builder = UserBuilder().with_name("Efim Sokolov").with_login("sokolcom").with_password("12345678")
        user_repo.register_user(*builder.build_register_data())
        return f(*args, **kwargs)

    return decorated_function


@clean_database
@register_erokha
def test_create_valid():
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    builder = WardrobeBuilder().with_name('name').with_creator_login('vkrivozubov').with_description('No desc')

    result, wardrobe_id = wardrobe_repo.create_wardrobe(*builder.build_create_data())

    assert result == "OK"
    assert wardrobe_id == 1


@clean_database
def test_create_invalid():
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    builder = WardrobeBuilder().with_name('name').with_creator_login('vkrivozubov').with_description('No desc')

    result = wardrobe_repo.create_wardrobe(*builder.build_create_data())

    assert result is None


@clean_database
@register_erokha
def test_get_by_id_valid():
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    builder = WardrobeBuilder().with_name('name').with_creator_login('vkrivozubov').with_description('No desc')
    expect = {"wardrobe_name": "name", "image_id": None, "image_url": None}

    _, wardrobe_id = wardrobe_repo.create_wardrobe(*builder.build_create_data())

    result = wardrobe_repo.get_wardrobe_by_id(wardrobe_id)

    assert result == expect


@clean_database
@register_erokha
def test_get_by_id_invalid():
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    builder = WardrobeBuilder().with_name('name').with_creator_login('vkrivozubov').with_description('No desc')

    _, wardrobe_id = wardrobe_repo.create_wardrobe(*builder.build_create_data())

    result = wardrobe_repo.get_wardrobe_by_id(wardrobe_id + 5)

    assert result is None


@clean_database
@register_erokha
def test_get_all_wardrobes_by_login_valid():
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    first_builder = WardrobeBuilder().with_name('name1').with_creator_login('vkrivozubov').with_description('No desc1')
    second_builder = WardrobeBuilder().with_name('name2').with_creator_login('vkrivozubov').with_description('No desc2')

    _, first_wardrobe_id = wardrobe_repo.create_wardrobe(*first_builder.build_create_data())
    _, second_wardrobe_id = wardrobe_repo.create_wardrobe(*second_builder.build_create_data())

    expect = [
        {
            'wardrobe_id': first_wardrobe_id,
            'image_id': None,
            'wardrobe_image': None,
            'wardrobe_name': first_builder.name,
            'wardrobe_description': first_builder.description,
            'wardrobe_owner': first_builder.creator_login
        },
        {
            'wardrobe_id': second_wardrobe_id,
            'image_id': None,
            'wardrobe_image': None,
            'wardrobe_name': second_builder.name,
            'wardrobe_description': second_builder.description,
            'wardrobe_owner': second_builder.creator_login
        }
    ]

    result = wardrobe_repo.get_all_wardrobes_by_login('vkrivozubov')

    assert result == expect


@clean_database
@register_erokha
def test_get_all_wardrobes_by_login_invalid():
    wardrobe_repo = WardrobeRepository(DB_NAME, False)

    result = wardrobe_repo.get_all_wardrobes_by_login('vkrivozubov123')

    assert len(result) == 0
