from typing import List, Union
import os
import pathlib
import subprocess
import random

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """ Subclass of IngestorInterface. Responsible for parsing PDF
    files into a list of quote objects.
    """
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: Union[str, pathlib.Path]) -> List[QuoteModel]:
        """ Overrides the parse() method of IngestorInterface. Uses
        subprocess to run XpdfReader to convert the PDF to a temporary
        text file. Then reads the text file and converts each line into
        quote objects.

        :param path: the file path
        :return: a list of QuoteModel objects
        """
        if not cls.can_ingest(path):
            raise Exception('File extension is not of type pdf')

        quotes = []
        path = pathlib.Path(path)
        tmp = path.parent.joinpath(f'{random.randint(0,100000)}.txt')

        try:
            subprocess.run(['pdftotext', '-layout', path, tmp])
            with open(tmp) as f:
                for line in f:
                    line = line.strip('\n\r').strip()
                    if len(line) > 0:
                        parse = line.split(" - ")
                        quotes.append(QuoteModel(parse[0], parse[1]))
            os.remove(tmp)
        except Exception as e:
            raise Exception(f'Error running subprocess pdftotext: {e}')

        return quotes
