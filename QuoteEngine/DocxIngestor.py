from typing import List, Union
from docx import Document
import pathlib

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class DocxIngestor(IngestorInterface):
    """ Subclass of IngestorInterface. Responsible for parsing DocX
    files into a list of quote objects.
    """
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: Union[str, pathlib.Path]) -> List[QuoteModel]:
        """ Overrides the parse() method of IngestorInterface. Uses
        docx to read the file line by line, converting each into quote
        objects.

        :param path: the file path
        :return: a list of QuoteModel objects
        """
        if not cls.can_ingest(path):
            raise Exception('File extension is not of type docx.')

        quotes = []
        try:
            doc = Document(path)
        except Exception as e:
            raise Exception(f'Error reading DocX file: {e}')
        else:
            for para in doc.paragraphs:
                if para.text != '':
                    parse = para.text.split(' - ')
                    quotes.append(QuoteModel(parse[0], parse[1]))

        return quotes
