from Repositories.LookRepository import LookRepository
from Repositories.UserRepository import UserRepository
from Repositories.ItemRepository import ItemRepository
from Repositories.WardrobeRepository import WardrobeRepository
from Test.DatabaseCleaner import DatabaseCleaner
from Test.Builders.LookBuilder import LookBuilder
from config import test_db_filename

DB_NAME = test_db_filename


def test_correct_add_look():
    DatabaseCleaner(DB_NAME).clean()
    username = "vkrivozubov"
    look_repo = LookRepository(DB_NAME, False)
    user_repo = UserRepository(DB_NAME, False)
    item_repo = ItemRepository(DB_NAME, False)
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    user_repo.register_user(username, "Vlad Krivozubov", "12345678", None)
    responseItem = item_repo.add_item(username, "some_name", "t-shirt", None)
    _, responseWardrobe = wardrobe_repo.create_wardrobe(username, "wardrobe_name", "description", None)
    look = LookBuilder().with_id(responseItem["item_id"]).with_name("cool_look")
    response = look_repo.create_look([look.clothes_id], look.look_name, responseWardrobe, None)
    assert look_repo.get_look_by_id(response["look_id"]) == [
        {'look_name': 'cool_look', 'image_id': None, 'image_url': None}]

def test_correct_update_look_test():
    DatabaseCleaner(DB_NAME).clean()
    username = "vkrivozubov"
    look_repo = LookRepository(DB_NAME, False)
    user_repo = UserRepository(DB_NAME, False)
    item_repo = ItemRepository(DB_NAME, False)
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    user_repo.register_user(username, "Efim Sokolov", "12345678", None)
    responseItem = item_repo.add_item(username, "some_name", "t-shirt", None)
    _, responseWardrobe = wardrobe_repo.create_wardrobe(username, "wardrobe_name", "description", None)
    look = LookBuilder().with_id(responseItem["item_id"]).with_name("cool_look")
    response = look_repo.create_look([look.clothes_id], look.look_name, responseWardrobe, None)
    assert look_repo.update_look(response["look_id"], "new_name", None) == {'status': 'OK'}
    assert look_repo.get_look_by_id(response["look_id"]) == [{'look_name': 'new_name', 'image_id': None, 'image_url': None}]

def test_correct_get_look_by_id_test():
    DatabaseCleaner(DB_NAME).clean()
    username = "vkrivozubov"
    look_repo = LookRepository(DB_NAME, False)
    user_repo = UserRepository(DB_NAME, False)
    item_repo = ItemRepository(DB_NAME, False)
    wardrobe_repo = WardrobeRepository(DB_NAME, False)
    user_repo.register_user(username, "Efim Sokolcom", "12345678", None)
    responseItem = item_repo.add_item(username, "item_name", "t-shirt", None)
    _, responseWardrobe = wardrobe_repo.create_wardrobe(username, "wardrobe_name", "description", None)
    response = look_repo.create_look([responseItem["item_id"]], "cool_look", responseWardrobe, None)
    assert look_repo.update_look(response["look_id"], "new_name", None) == {'status': 'OK'}