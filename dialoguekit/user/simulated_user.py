from dialoguekit.user.user import User, UserType

class SimulatedUser(User):

    def __init__(self) -> None:
        self._user_type = UserType.SIMULATOR
        # TODO(to include)
        # - PKG
        # - NLU/NLG
