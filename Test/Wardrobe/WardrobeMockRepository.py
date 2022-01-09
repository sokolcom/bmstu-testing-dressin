from typing import Optional, Tuple, List

from Repositories.WardrobeRepository import IWardrobeRepository


class WardrobeMockRepository(IWardrobeRepository):

    def __init__(self):
        pass

    def create_wardrobe(self, login, name, description=None, image=None) -> Optional[Tuple[str, int]]:
        pass

    def share_wardrobe(self, wardrobeid, invite_login) -> Optional[str]:
        pass

    def get_all_wardrobes_by_login(self, login) -> List[dict]:
        pass

    def delete_wardrobe(self, wardrobe_id, login) -> Optional[str]:
        pass

    def remove_user_from_wardrobe(self, wardrobe_id, login) -> Tuple[dict, bool]:
        pass

    def get_wardrobe_by_id(self, wardrobe_id) -> Optional[dict]:
        pass

    def update_wardrobe(self, wardrobe_id, new_name, image_id) -> Optional[str]:
        pass

    def get_photo_id_by_wardrobe_id(self, look_id) -> Optional[int]:
        pass

    def is_key_valid(self, key):
        pass