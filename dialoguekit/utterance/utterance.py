from enum import Enum

class UtteranceType(Enum):

    WELCOME = 0
    MESSAGE = 1
    EXIT = 2


class Utterance:
    def __init__(self, text: str, utterance_type : UtteranceType=UtteranceType.MESSAGE):
        self._text = text
        self._utterance_type = utterance_type

    @property
    def text(self):
        return self._text

    @property
    def utterance_type(self):
        return self._utterance_type
