import pathlib

# project root directory
ROOT_DIR = pathlib.Path(__file__).parent
# path for newly generated meme images
STATIC_DIR = pathlib.Path(ROOT_DIR).joinpath('static')
# path for quotes files for generating memes
QUOTES_DIR = pathlib.Path(ROOT_DIR).joinpath('_data/DogQuotes')
# path for input image files for generating memes
IMAGES_DIR = pathlib.Path(ROOT_DIR).joinpath('_data/photos/dog')
# path for temp storage of user-supplied images for meme creation
TEMP_DIR = pathlib.Path(ROOT_DIR).joinpath('_data/temp')
# fonts path
FONTS_DIR = pathlib.Path(ROOT_DIR).joinpath('fonts')
