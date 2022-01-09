from Repositories.ItemRepository import IItemRepository
from typing import Optional

class ItemMockRepository(IItemRepository):
    def get_item_by_id(self, item_id) -> Optional[dict]:
        pass

    def add_item(self, owner, name, type, image_id=None) -> Optional[dict]:
        pass

    def update_item(self, item_id, new_name, id) -> Optional[dict]:
        pass

    def remove_item(self, item_id) -> Optional[str]:
        pass

    def get_all_items_by_user(self, login) -> Optional[dict]:
        pass

    def get_photo_id_by_item_id(self, item_id) -> Optional[int]:
        pass