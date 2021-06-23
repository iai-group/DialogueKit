"""Interface representing annotations."""


class Annotation:
    """Represents an annotation."""

    def __init__(
        self,
        slot: str = None,
        value: str = None,
        start: int = None,
        end: int = None,
    ) -> None:
        # TODO: slot should refer to a class in Ontology

        self.__slot = slot
        self.__value = value
        self.__start = start
        self.__end = end
