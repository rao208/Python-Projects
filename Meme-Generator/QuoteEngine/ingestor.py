from typing import List
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .docx_ingestor import DocxIngestor
from .csv_ingestor import CSVIngestor
from .pdf_ingestor import PDFIngestor
from .text_ingestor import TextIngestor


class Ingestor(IngestorInterface):

    '''This class inherits from the IngestorInterface.
    It calls all the other ingestor classes.

    Arguments:
    ----------------------
    ingestors {list} -- a class variable which specifies
    other ingestor classes.

    Methods:
    -----------------------
    parse(path): a class method

    Returns results from the required ingestor.

    '''

    ingestors = [DocxIngestor, CSVIngestor, PDFIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        '''Returns results from the required ingestor.

        Arguments:
        -----------------------
        path{str}-- path of the file

        '''
        for ingestors in cls.ingestors:
            if ingestors.can_ingest(path):
                return ingestors.parse(path)
