import Repositories.LookRepository as repository
from Repositories.ImageRepository import ImageRepository
from Repositories.LookRepository import LookRepository
import json_routine as js


class LookService:
    repo: repository.ILookRepository

    def __init__(self, repo: repository.ILookRepository):
        self.repo = repo

    def create_look(self, item_ids, look_name, wardrobe_id, image):
        if image != None:
            image = ImageRepository().save_photo(image)
        else:
            image = None
        response = self.repo.create_look(item_ids, look_name, wardrobe_id, image)
        response_code = 200 if response and response != {} else 500
        return js.getJSON(response), response_code

    def change_look(self, look_id, new_name, image):
        if image != None:
            id = self.repo.get_photo_id_by_look_id(look_id)
            if id:
                id = ImageRepository().update_photo(id, image)
            else:
                id = ImageRepository().save_photo(image)
        else:
            id = None
        response = self.repo.update_look(look_id, new_name, id)
        response_code = 200 if response else 500
        return js.getJSON({"status": response}), response_code

    def get_look_by_id(self, look_id):
        response = self.repo.get_look_by_id(look_id)
        response_code = 200 if response else 500
        return js.getJSON(response), response_code




