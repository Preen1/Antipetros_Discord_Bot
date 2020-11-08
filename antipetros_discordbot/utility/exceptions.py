
class AntiPetrosBaseError(Exception):
    pass


class TokenError(AntiPetrosBaseError):
    __module__ = 'antipetros-discordbot'

    def __init__(self, in_message):
        super().__init__(in_message)
