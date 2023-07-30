from typing import List
import docx
from .ingestor_interface import IngestorInterface
from .quote_model import QuoteModel
from .exception import InvalidFileExtension

class DocxIngestor(IngestorInterface):

    '''This ingestor overrides the parse method to read docx files and
    extract lines. It uses the python-docx library to read DOCX files.

    Arguments:
    ----------------------
    allowed_extenstion {list}-- a class variable which specifies
    the file extension that are allowed for this class

    '''

    allowed_extension = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        '''Returns quotes with body and the author from the docx file

        Arguments:
        ----------------
        path {str}-- path of the docx file

        Raises:
        ------------------
        Exception: when the path cannot be ingested

        '''

        if not cls.can_ingest(path):
            raise InvalidFileExtension('cannot ingest exception')

        quotes = []
        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                parse = para.text.split('-')
                new_quotes = QuoteModel(parse[0], parse[1])
                quotes.append(new_quotes)

        return quotes
