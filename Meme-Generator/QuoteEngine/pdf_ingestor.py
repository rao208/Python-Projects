from typing import List
import subprocess
import os
import random
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .text_ingestor import TextIngestor
from .exception import InvalidFileExtension

class PDFIngestor(IngestorInterface):

    '''This ingestor overrides the parse method to read PDF files and extract
    its lines into a text file. That text file is then parsed using the
    TextIngestor. It uses the subprocess library to call the pdftotext
    command line tool to extract text from PDF into a .txt file.

    Arguments:
    ----------------------
    allowed_extenstion {list}-- a class variable which specifies
    the file extension that are allowed for this class

    '''

    allowed_extension = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        '''Returns quotes with body and the author from the pdf file

        Arguments:
        ----------------
        path {str}-- path of the pdf file

        Raises:
        ------------------
        Exception: when the path cannot be ingested

        '''

        if not cls.can_ingest(path):
            raise InvalidFileExtension('cannot ingest exception')

        tmp = f'./tmp/{random.randint(0,1000000)}.txt'
        subprocess.call(['pdftotext', path, tmp])

        quotes = TextIngestor.parse(tmp)
        os.remove(tmp)

        return quotes
