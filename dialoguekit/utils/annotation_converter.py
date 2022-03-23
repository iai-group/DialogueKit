"""Annotation converter interface.

As the different modules used for NLU use different formats for training file
converters are needed."""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class AnnotationConverter(ABC):
    """Annotation converter interface.

    Attributes:
        filepath: String path to the original annotation file.
        save_to_path: Optional String path to the destination directory.
    """

    def __init__(
        self, filepath: str, save_to_path: Optional[str] = None
    ) -> None:
        self._filepath = filepath
        self._save_to_path = save_to_path
        self._converted = {}

    @abstractmethod
    def run(self) -> Dict[str, str]:
        """Runs the converter.

        The conversion will run and save to 'save_to_path' directory. If the
        converter supports different file outputs, this method will run all the
        supported conversions.

        Returns:
            Dictionary with filename and filepath pairs.

        Raises:
            NotImplementedError
        """

        raise NotImplementedError
