from typing import List, Union
import pandas
import pathlib

from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    """ Subclass of IngestorInterface. Responsible for parsing CSV
    files into a list of quote objects.
    """
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: Union[str, pathlib.Path]) -> List[QuoteModel]:
        """ Overrides the parse() method of IngestorInterface. Uses
        pandas to convert the csv data into dataframe rows, each of
        which then are converted into quote objects.

        :param path: the file path
        :return: a list of QuoteModel objects
        """
        if not cls.can_ingest(path):
            raise Exception('File extension is not of type csv')

        quotes = []
        try:
            df = pandas.read_csv(path, header=0)
        except Exception as e:
            raise Exception(f'Error reading CSV file: {e}')
        else:
            for index, row in df.iterrows():
                quotes.append(QuoteModel(row.iloc[0], row.iloc[1]))

        return quotes
