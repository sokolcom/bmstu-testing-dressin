import json_routine
from Repositories.ImageRepository import IImageRepository, ImageRepository
from Repositories.WardrobeRepository import IWardrobeRepository


class WardrobeService:
    repo: IWardrobeRepository
    image_repo: IImageRepository

    def __init__(self, repo: IWardrobeRepository, image_repo: IImageRepository = ImageRepository()):
        self.repo = repo
        self.image_repo = image_repo

    def get_wardrobes(self, login):
        try:
            self.repo.get_all_wardrobes_by_login(login)
        except Exception as e:
            print(f'WardrobeService.get_wardrobes: {e}')
            return None, 500

    def get_wardrobe_by_id(self, id):
        if id is None:
            return json_routine.getJSON({"status": "error", "reason": "Incorrect input data"}), 405
        response = self.repo.get_wardrobe_by_id(id)
        response_code = 200 if response else 500
        return json_routine.getJSON(response), response_code

    def create_wardrobe(self, login, wardrobe_name, wardrobe_description, file):
        try:
            image = self.image_repo.save_photo(file)
        except Exception:
            image = None
        finally:
            response = self.repo.create_wardrobe(login, wardrobe_name, wardrobe_description, image)
            if response is None:
                return json_routine.getJSON({"status": "error", "reason": "internal server error"}), 500
            status, _ = response
            response_code = 200 if status == "OK" else 500
            return json_routine.getJSON({"status": status}), response_code

    def delete_wardrobe(self, wardrobe_id, login):
        status = self.repo.delete_wardrobe(wardrobe_id, login)
        if status and status == "OK":
            return json_routine.getJSON({"status:": status}), 200
        else:
            return json_routine.getJSON({"status:": "error", "reason": "Internal server error"}), 500

    def remove_user_from_wardrobe(self, wardrobe_id, login):
        response, error = self.repo.remove_user_from_wardrobe(wardrobe_id, login)
        if not error:
            return json_routine.getJSON(response), 200
        try:
            response_code = 405 if "Not owner tried" in response["reason"] else 500
            return json_routine.getJSON(response), response_code
        except Exception:
            return json_routine.getJSON(response), 500

    def update_wadrobe(self, wardrobe_id, new_name, image):
        try:
            id = self.repo.get_photo_id_by_wardrobe_id(wardrobe_id)
            if id:
                id = self.image_repo.update_photo(id, image)
            else:
                id = self.image_repo.save_photo(image)
        except Exception:
            id = None
        response = self.repo.update_wardrobe(wardrobe_id, new_name, id)
        respcode = 200 if response else 500
        status = response if response else "error"
        return json_routine.getJSON({"status": status}), respcode