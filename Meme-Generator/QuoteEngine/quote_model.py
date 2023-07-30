class QuoteModel:
    '''QuoteModel class encapsulates the body and the author'''

    def __init__(self, body, author):
        '''Create a QuoteModel class.

        Arguments:
        body{str} -- the quote for the meme
        author{str} -- the author of the quote

        '''
        self.body = body
        self.author = author

    def __repr__(self):
        return f'{self.body}-{self.author}'
