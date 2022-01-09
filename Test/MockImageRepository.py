from Repositories.ImageRepository import IImageRepository


class MockImageRepository(IImageRepository):

    def __init__(self):
        pass

    def save_photo(self, photo):
        pass

    def update_photo(self, id, data):
        pass

    def get_photo(self, id):
        pass

    def update_user_photo(self, id, data):
        pass
