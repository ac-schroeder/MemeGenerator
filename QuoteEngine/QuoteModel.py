class QuoteModel():

    def __init__(self, body: str, author: str) -> None:
        """ Construct a Quote object containing the text body
        of the quote and the author.

        :param body: the text of the quote
        :param author: the author of the quote
        """
        body = body.strip('"')
        self.body = f'"{body}"'
        self.author = author

    def __repr__(self) -> str:
        """ Return a computer-readable string representation of
        this quote object.

        :return: string representation of the quote object
        """
        return f'<{self.body}, {self.author}>'

    def __str__(self) -> str:
        """ Return a string representation of this quote object.

        :return: string representation of the quote object
        """
        return f'{self.body} - {self.author}'
