from typing import List
import pandas
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
import os
from .exception import FileNotFound
from .exception import InvalidFileExtension
from .exception import EmptyFile


class CSVIngestor(IngestorInterface):

    '''This ingestor overrides the parse method to read CSV
    files and extract lines. It uses pandas library to read CSV file

    Arguments:
    ----------------------
    allowed_extenstion {list}-- a class variable which specifies
    the file extension that are allowed for this class

    '''

    allowed_extension = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        '''Returns quotes with body and the author from the csv file

        Arguments:
        ----------------
        path {str}-- path of the csv file

        Raises:
        ------------------
        Exception: when the path cannot be ingested

        Exception handling:
        --------------------
        when the file cannot be found
        when the csv file is empty
        when the csv file is not loaded

        ''' 

        quotes = []

        try:

            df = pandas.read_csv(path, header=0)

        except Exception:

            raise FileNotFound("Input file not found: {}".format(path))

        except Exception:

            if cls.can_ingest(path):
                if os.stat(path).st_size == 0:
                    raise EmptyFile(("The CSV file is empty."
                                    "No columns to parse from file"))
            else:
                raise InvalidFileExtension('cannot ingest exception')

        else:

            for index, row in df.iterrows():
                new_quotes = QuoteModel(row['body'], row['author'])
                quotes.append(new_quotes)

            return quotes
