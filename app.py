from typing import Union
from constants import ROOT_DIR, STATIC_DIR, QUOTES_DIR, \
                      IMAGES_DIR, TEMP_DIR
from flask import Flask, render_template, request
import random
import os
import requests

from MemeEngine import MemeEngine
from QuoteEngine import Ingestor

app = Flask(__name__)
meme = MemeEngine(STATIC_DIR)


def setup():
    """ Load all quotes and image resources used for random meme
    generation. Search the quotes and images directories for
    supported file types and compile lists of the resources. For
    quotes, call the QuoteEngine module to parse the contents of
    the quotes files.

    :return: A list of quote objects and a list of image paths
    """

    # Parse all quotes files and save as a list of quotes.
    quotes = []
    for item in os.listdir(QUOTES_DIR):
        file_path = QUOTES_DIR.joinpath(item)
        if os.path.isfile(file_path):
            try:
                quotes.extend(Ingestor.parse(file_path))
            except Exception as e:
                print(f'Ingestor Error:  {e}')

    # Alert if no quotes could be loaded.
    if not quotes:
        print('Warning: No Default Quotes!')

    # Get list of all paths for default meme images.
    imgs = []
    for item in os.listdir(IMAGES_DIR):
        file_path = IMAGES_DIR.joinpath(item)
        valid_extensions = ['.jpg', '.jpeg', '.png', '.svg', '.webp']
        if file_path.suffix in valid_extensions:
            imgs.append(file_path)

    # Alert if no image paths could be found.
    if not imgs:
        print('Warning: No Default Images!')

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme. """

    # If no default quotes or images could be found,
    # load the create meme page instead.
    if not quotes or not imgs:
        print('Warning: No Default Quotes or Images!')
        return render_template('meme_form.html')

    # Use a random image and quote to create a meme.
    img = random.choice(imgs)
    quote = random.choice(quotes)
    rel_path = None
    try:
        path = meme.make_meme(img, quote.body, quote.author)
        rel_path = path.relative_to(ROOT_DIR)
    except Exception as e:
        print(f'Error making meme: {e}')

    return render_template('meme.html', path=rel_path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ Display form to get user-supplied meme information. """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme. """

    # Get the form inputs.
    img_url = request.form['image_url'].strip()
    quote_body = request.form['body'].strip()
    quote_author = request.form['author'].strip()

    # Validate form inputs and redisplay form if missing data.
    error = validate_form_inputs(img_url, quote_body, quote_author)
    if error:
        return render_template('meme_form.html', error_message=error)

    # Retrieve the user's image.
    r = requests.get(img_url)
    tmp_img = TEMP_DIR.joinpath(f'{random.randint(1, 1000000)}.png')
    with open(tmp_img, 'wb') as f:
        f.write(r.content)

    # Convert the image to a meme.
    rel_path = None
    try:
        path = meme.make_meme(tmp_img, quote_body, quote_author)
        rel_path = path.relative_to(ROOT_DIR)
    except Exception as e:
        print(f'Error making meme: {e}')

    # Remove the temporary image.
    os.remove(tmp_img)

    # Render the template with the new meme path.
    return render_template('meme.html', path=rel_path)


def validate_form_inputs(img_url: str,
                         quote_body: str,
                         quote_author: str) -> Union[str, None]:
    """ Check that all inputs are complete.

    :param img_url: the form input of the url of the image
    :param quote_body: the form input of the text of the quote
    :param quote_author: the form input of the author of the quote
    :return: an error message, or None if no error
    """
    # Check all fields are complete.
    if not img_url or not quote_body or not quote_author:
        return 'Please fill in all fields.'
    return None


if __name__ == "__main__":
    app.run()
