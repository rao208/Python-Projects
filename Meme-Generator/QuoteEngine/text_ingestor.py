from typing import List
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
import os


class TextIngestor(IngestorInterface):

    '''This ingestor overrides the parse method to read text files and
    extract lines. It uses the in-built file reading methods to read
    text files.

    Arguments:
    ----------------------
    allowed_extenstion {list}-- a class variable which specifies
    the file extension that are allowed for this class

    '''

    allowed_extension = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        '''Returns quotes with body and the author from the text file

        Arguments:
        ----------------
        path {str}-- path of the text file

        '''

        if not os.path.exists(path):
            os.makedirs(path)

        file_ref = open(path, "r")
        quotes = []

        for quote in file_ref.readlines():
            quote = quote.strip('\n\r').strip()
            if len(quote) > 0:
                parse = quote.split('-')
                new_quotes = QuoteModel(parse[0], parse[1])
                quotes.append(new_quotes)

            file_ref.close()

        return quotes
