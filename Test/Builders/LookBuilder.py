class LookBuilder:
    clothes_id = []
    look_name = ""
    image = None

    def with_id(self, ids):
        self.clothes_id = ids
        return self

    def with_name(self, name):
        self.look_name = name
        return self