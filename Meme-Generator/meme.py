import os
import random
import argparse
from QuoteEngine.ingestor import Ingestor
from QuoteEngine.quote_model import QuoteModel
from MemeEngine.meme_engine import MemeEngine


def generate_meme(path=None, body=None, author=None):
    '''Generate a meme given an path and a quote'''

    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv',
                       './_data/DogQuotes/DogQuotesTXT.txt']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeEngine('./tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file

    parser.add_argument("--path",
                        nargs="+",
                        type=str,
                        default=None,
                        required=False,
                        help="Please upload an image for your meme")

    # body - quote body to add to the image

    parser.add_argument("--body",
                        type=str,
                        default=None,
                        required=False,
                        help="Meme content")

    # author - quote author to add to the image

    parser.add_argument("--author",
                        type=str,
                        help="The author of the meme")

    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
