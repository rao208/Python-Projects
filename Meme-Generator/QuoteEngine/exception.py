class FileNotFound(Exception):
    '''Raised when the file is not found'''
    pass


class InvalidFileExtension(Exception):
    '''Raised when the file has invalid extenstion'''
    pass


class EmptyFile(Exception):
    '''Raised when the file is empty'''
    pass
