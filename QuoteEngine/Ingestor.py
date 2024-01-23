from typing import List, Union
import pathlib

from .IngestorInterface import IngestorInterface
from .CSVIngestor import CSVIngestor
from .DocxIngestor import DocxIngestor
from .PDFIngestor import PDFIngestor
from .TextIngestor import TextIngestor
from .QuoteModel import QuoteModel


class Ingestor(IngestorInterface):
    """ Subclass of IngestorInterface. Responsible for choosing
    which specific ingestor subclass should be called upon to parse a
    file into quote objects.

    It contains a list of all ingestor subclasses. When this class is
    called upon to parse a file, it checks each ingestor subclass's
    can_ingest() method on the file, to determine which one it should
    call to parse the file.
    """

    ingestors = [CSVIngestor, DocxIngestor,
                 PDFIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: Union[str, pathlib.Path]) -> List[QuoteModel]:
        """Overrides the parse() method of IngestorInterface. It
        checks the input file against each ingestor subclass's
        can_parse() method. When it finds an ingestor that can parse
        the file, it calls that ingestor's parse() method on the file.

        :param path: a path to a quotes file
        :return: a list of quotes
        """
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
