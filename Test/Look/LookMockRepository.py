from Repositories.LookRepository import ILookRepository
from typing import Optional

class LookMockRepository(ILookRepository):
    def is_key_valid(self, key):
        pass

    def get_look_by_wardrobe(self, wardrobe_id):
        pass

    def create_look(self, item_ids, look_name, wardrobe_id, image=None) -> Optional[dict]:
        pass

    def get_look_items(self, look_id):
        pass

    def append_items_into_look(self, look_id, item_id):
        pass

    def update_look_items(self, look_id, item_ids):
        pass

    def remove_item_from_look_by_id(self, look_id, item_id):
        pass

    def get_look_by_id(self, look_id) -> Optional[dict]:
        pass

    def update_look(self, look_id, new_name, image_id):
        pass

    def remove_look(self, look_id):
        pass

    def get_photo_id_by_look_id(self, look_id):
        pass