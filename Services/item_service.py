import Repositories.ItemRepository as repository
from Repositories.ImageRepository import IImageRepository
import json_routine as js


class ItemService:
    repo: repository.IItemRepository
    image_repo: IImageRepository

    def __init__(self, repo: repository.IItemRepository, image_repo: IImageRepository):
        self.repo = repo
        self.image_repo = image_repo

    def get_item_by_id(self, id):
        response = self.repo.get_item_by_id(id)
        respose_code = 200 if response else 500
        return js.getJSON(response), respose_code

    def remove_item(self, id):
        response = self.repo.remove_item(id)
        respose_code = 200 if response else 500
        return js.getJSON({"status": response}), respose_code

    def add_item(self, item_name, login, type, file):
        if file != None:
            id = self.image_repo.save_photo(file)
        else:
            id = None
        response = self.repo.add_item(login, item_name, type, id)
        respose_code = 200 if response and response != {} else 500
        return js.getJSON(response), respose_code

    def update_item(self, item_id, new_name, file):
        try:
            image_id = self.repo.get_photo_id_by_item_id(item_id)
            if image_id:
                image_id = self.image_repo.update_photo(image_id, file)
            else:
                image_id = self.image_repo.save_photo(file)
        except Exception:
            image_id = None
        response = self.repo.update_item(item_id, new_name, image_id)
        respose_code = 200 if response else 500
        return js.getJSON({"status": response}), respose_code
