from Repositories.InviteRepository import IInviteRepository


class InviteMockRepository(IInviteRepository):

    def get_wardrobe_editors(self, wardrobe_id):
        pass

    def get_invites_by_login(self, login):
        pass

    def inviteUser(self, my_login, login_whom_to_inivte, wardrobe_id):
        pass

    def handleInvite(self, invite_id, accepted):
        pass

    def is_key_valid(self, key):
        pass