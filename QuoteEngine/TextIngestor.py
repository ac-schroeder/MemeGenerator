from typing import List, Union
import pathlib

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TextIngestor(IngestorInterface):
    """ Subclass of IngestorInterface. Responsible for parsing text
    files into a list of quote objects.
    """
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: Union[str, pathlib.Path]) -> List[QuoteModel]:
        """ Overrides the parse() method of IngestorInterface. Reads
        the text file and converts each line into quote objects.

        :param path: the file path
        :return: a list of QuoteModel objects
        """
        if not cls.can_ingest(path):
            raise Exception('File extension is not of type txt')

        quotes = []
        try:
            with open(path, encoding='utf-8-sig') as f:
                for line in f:
                    line = line.strip('\n\r').strip()
                    if len(line) > 0:
                        parse = line.split(" - ")
                        quotes.append(QuoteModel(parse[0], parse[1]))
        except Exception as e:
            raise Exception(f'Error reading text file: {e}')

        return quotes
