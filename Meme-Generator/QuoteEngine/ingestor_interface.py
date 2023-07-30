from abc import ABC, abstractmethod
from typing import List
from .quote_model import QuoteModel


class IngestorInterface(ABC):

    '''This class is an interface that is used as a base class for
    all other ingestors.

    Arguments:
    ------------------
    allowed_extenstion {list}-- a class variable which specifies
    the file extension that are allowed.

    Methods:
    --------------------
    can_ingest(path)--
    A class method to check if a file extension is supported or not.

    parse(path)--
    An abstract class method that is used by the child classes to parse files.
    '''

    allowed_extension = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:

        '''Returns True if the file extension is supported
        False if the file extension is not supported

        Argument:
        --------------------
        path{str}-- the path of the file

        '''
        ext = path.split('.')[-1]
        return ext in cls.allowed_extension

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        '''Returns quotes with body and the author from the file

        Arguments:
        ----------------
        path {str}-- path of the file

        '''

        pass
