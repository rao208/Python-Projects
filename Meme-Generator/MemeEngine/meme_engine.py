from PIL import Image, ImageDraw, ImageFont
import os
import random
from QuoteEngine.exception import FileNotFound
import textwrap
from string import ascii_letters


class MemeEngine():

    '''The engine behind meme generation

    Arguments:
    -------------
    output_dir {str} -- Output directory path to save the meme

    Method:
    --------------
    make_meme(img_path, body, author, width=500)--
    returns the output path {str} of the meme

    '''

    def __init__(self, output_dir):

        '''Contructs all the necessary attributes for the MemeEngine object

        Arguments:
        ----------------
        output_dir {str} -- Output directory path to save the meme

        '''

        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def make_meme(self, img_path, body, author, width=500) -> str:

        '''Returns output path {str} of the meme

        Arguments:
        -------------------
        img_path {str}-- An image path to load the image for the meme.
        body {str}-- The body of the meme. It is placed on the top of
        the image.

        author{str}-- The author of the body of the meme. It is located
        on the bottom of the image.

        width{int}-- to transform image by resizing to a width while
        maintaining the input aspect ratio. Maximum width is 500px (default)

        Raises:
        ----------------------

        Exception: FileNotFound

        '''

        try:
            img = Image.open(img_path)

        except Exception:

            raise FileNotFound("Input file not found: {}".format(img_path))

        else:

            temp_name = random.randint(0, 100000000)
            out_path = os.path.join(self.output_dir,
                                    f"temp-{temp_name}.jpg")
            if width is not None:

                ratio = width/float(img.size[0])
                height = int(ratio*float(img.size[1]))
                img.thumbnail((width, height))

            draw = ImageDraw.Draw(img)

            if body is not None:

                font_body = ImageFont.truetype(
                    './_data/fonts/times new roman.ttf', size=20)

                wrapped_text = textwrap.fill(text=body, width=30)
                text_w, text_h = draw.textsize(wrapped_text, font_body)

                draw.text(xy=((width-text_w)//2, (height - text_h)//text_h),
                          text=wrapped_text,
                          fill="red",
                          font=font_body,
                          anchor='mm')

            if author is not None:

                font_author = ImageFont.truetype(
                    './_data/fonts/times new roman italic.ttf', size=20)

                wrapped_text = textwrap.fill(text=author, width=30)
                text_w, text_h = draw.textsize(wrapped_text, font_author)

                draw.text(xy=((width - text_w)//2, (height - text_h)),
                          text=wrapped_text,
                          fill="red",
                          font=font_author)
            img.save(out_path)

            return out_path
