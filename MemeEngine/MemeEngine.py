from typing import Union
from PIL import Image, ImageFont, ImageDraw
import random
import pathlib


class MemeEngine():
    """ An engine for creating memes based on provided images an
    quotes.

    The MemeEngine uses the Pillow library to convert a provided image
    into a meme image with overlaid text for a quote caption, sized to
    the specified dimensions. It will wrap long quote text to fit the
    image.

    The MemeEngine saves created memes at the location stored in its
    output_dir attribute, set upon initialisation of the object.
    """

    def __init__(self,
                 output_dir: Union[str, pathlib.Path]) -> None:
        """ Construct a new MemeEngine with the specified output
        directory for any generated memes.

        :param output_dir: The location to save generated memes
        """
        self.output_dir = pathlib.Path(output_dir)

    def make_meme(self,
                  img_path: Union[str, pathlib.Path],
                  text: str,
                  author: str,
                  width: int = 500) -> pathlib.Path:
        """ Create a meme image from the supplied components.

        :param img_path: the path to the image on disk
        :param text: the body of the quote for the caption
        :param author: the author of the quote for the caption
        :param width: the resize width of the image, defaults to 500
        :return: the generated image path as a string
        """
        # Load image file from disk.
        with Image.open(img_path) as im:
            
            # Resize the image
            resize_ratio = width/im.width
            im = im.resize((width, int(im.height * resize_ratio)),
                           Image.NEAREST)

            # Set a random text anchor position for the caption
            text_y = random.uniform(0.1, 0.7) * im.height
            text_x = random.uniform(0.1, 0.3) * im.width
            text_anchor = (text_x, text_y)

            # Set the text width and wrap the caption to fit
            caption = f'{text} - {author}'            
            font = ImageFont.truetype('./fonts/LilitaOne-Regular.ttf', 22)
            text_width = (im.width - text_x) * 0.8
            caption = self.get_wrapped_text(caption, font, text_width)

            # Draw the caption
            draw = ImageDraw.Draw(im)  
            draw.text(text_anchor, caption, fill='white', font=font)

            # Save the file to the chosen output directory
            out_file = f'{random.randint(0,100000000)}.png'
            out_path = self.output_dir.joinpath(out_file)
            im.save(out_path, format='PNG')

        return out_path

    # Function shared by Chris Collett on StackOverflow, Apr 21, 2021
    # https://stackoverflow.com/a/67203353
    def get_wrapped_text(self,
                         text: str,
                         font: ImageFont.ImageFont,
                         line_length: int) -> str:
        """ Wraps the provided text to fit the given line length.
        Does not split in the middle of a word.

        Function by Chris Collett on StackOverflow, Apr 21,
        2021: https://stackoverflow.com/a/67203353

        :param text: The text to wrap
        :param font: The font of the text, which affects its size
        :param line_length: The number of pixels of space for the line
        :return: A string of wrapped text, containing line breaks
                 where needed to fit the line length.
        """
        lines = ['']
        for word in text.split():
            # Add the next word to the current line
            line = f'{lines[-1]} {word}'.strip()
            # Check if the current line is getting too long
            if font.getlength(line) <= line_length:
                # Save the line with the new word at the end
                lines[-1] = line
            else:
                # Start a new line beginning with this word
                lines.append(word)
        return '\n'.join(lines)
