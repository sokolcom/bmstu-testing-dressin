from Repositories.ItemRepository import ItemRepository
from Repositories.UserRepository import UserRepository
from Test.DatabaseCleaner import DatabaseCleaner
from config import test_db_filename

DB_NAME = test_db_filename

def test_correct_add_item():
    DatabaseCleaner(DB_NAME).clean()
    item_repo = ItemRepository(DB_NAME, False)
    user_repo = UserRepository(DB_NAME, False)
    username = "vkrivozubov"
    user_repo.register_user(username, "Vlad Krivozubov", "12345678", None)
    response = item_repo.add_item(username, 'some_name', 't-shirt', None)
    assert response == {"item_id": 1}
    response = item_repo.get_item_by_id(1)
    assert response == {'clothes_id': 1, 'clothes_name': 'some_name', 'type': 't-shirt', 'image_id': None,
                        'owner_login': username, 'image_url': None}

def test_incorrect_add_item_from_invalid_user():
    DatabaseCleaner(DB_NAME).clean()
    item_repo = ItemRepository(DB_NAME, False)
    username = "no such user"
    response = item_repo.add_item(username, 'some_name', 't-shirt', None)
    assert response is None

def test_correct_remove_item():
    DatabaseCleaner(DB_NAME).clean()
    item_repo = ItemRepository(DB_NAME, False)
    assert item_repo.remove_item(1) is not None
    assert item_repo.get_item_by_id(1) is None

def test_correct_update_item():
    DatabaseCleaner(DB_NAME).clean()
    item_repo = ItemRepository(DB_NAME, False)
    user_repo = UserRepository(DB_NAME, False)
    username = "sokolcom"
    user_repo.register_user(username, "Efim Sokolov", "12345678", None)
    responsItemAdd = item_repo.add_item(username, 'some_name', 't-shirt', None)
    item_repo.update_item(responsItemAdd["item_id"], "new_name", None)
    assert item_repo.get_item_by_id(responsItemAdd["item_id"]) == {'clothes_id': 1, 'clothes_name': 'new_name', 'type': 't-shirt', 'image_id': None, 'owner_login': 'sokolcom', 'image_url': None}
