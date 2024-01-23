from abc import ABC, abstractmethod
from typing import List, Union
import pathlib

from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """ Abstract superclass for different types of file ingestors
    (parsers). An ingestor checks whether a file type is supported
    and then parses it line by line to package as quote objects
    for the meme generator.

    The allowed_extensions attribute should be overridden by
    child ingestor classes to suit each specific type of ingestor
    (i.e. csv, pdf, etc).

    The parse() method should be overridden with the filetype-specific
    implementation to read the given file line by line.
    """
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: Union[str, pathlib.Path]) -> bool:
        """ Checks whether the provided file has a supported
        extension.

        :param path: the file path
        :return: boolean: whether the file is supported
        """
        ext = str(path).split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: Union[str, pathlib.Path]) -> List[QuoteModel]:
        """ Parse the provided file into a list of quote objects.

        Concrete subclasses must override this method with specific
        implementation depending on file type.

        :param path: the file path
        :return: a list of quotes
        """
        raise NotImplementedError
