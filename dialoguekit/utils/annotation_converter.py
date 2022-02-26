""" Annotation converter interface

Used as the interface for annotation converters.
As the different modules used for nlu use different
formats for training file converters are needed"""

from abc import ABC, abstractmethod
from typing import Dict, Optional


class AnnotationConverter(ABC):
    """Annotation converter interface

    Attributes:
        filepath: String path to the original annotation file
        save_to_path: Optional String path to the destination directory
    """

    def __init__(
        self, filepath: str, save_to_path: Optional[str] = None
    ) -> None:
        self.filepath = filepath
        self.save_to_path = save_to_path
        self.converted = {}

    @abstractmethod
    def run(self) -> Dict[str, str]:
        """Method to run the converter

        The conversion will run and save to 'save_to_path' directory.
        If the converter supports different file outputs, this
        method will run all the supported conversions.

        Returns:
            Dict[str:str]: dictionary with filename and filepaths.


        Raises:
            NotImplementedError: _description_
        """

        raise NotImplementedError
