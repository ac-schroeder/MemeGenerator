import unittest
import pathlib
import os
from PIL import Image, ImageChops

from MemeEngine import MemeEngine

TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_MEMES_DIR = TESTS_ROOT.joinpath('Memes')
TEST_IMAGE = TESTS_ROOT.joinpath('DogImages/test_image.jpg')
TEST_MEME = TEST_MEMES_DIR.joinpath('expected_meme.png')


class TestMemeEngine(unittest.TestCase):

    def setUp(self) -> None:
        self.meme = MemeEngine(TEST_MEMES_DIR)

    def test_meme_engine_returns_image_path(self):
        text = 'Life is like peanut butter: crunchy'
        author = 'Peanut'
        generated_meme = self.meme.make_meme(TEST_IMAGE,
                                             text, author,
                                             width=500)

        self.assertIsInstance(generated_meme, pathlib.Path)
        self.assertEqual(generated_meme.suffix, '.png')

        os.remove(generated_meme)

    def test_meme_engine_returns_expected_image(self):
        text = 'Life is like peanut butter: crunchy'
        author = 'Peanut'
        generated_meme = self.meme.make_meme(TEST_IMAGE,
                                             text, author,
                                             width=500)

        expected_img = Image.open(TEST_MEME).convert("RGB")
        generated_img = Image.open(generated_meme).convert("RGB")

        diff = ImageChops.difference(expected_img, generated_img)
        self.assertIsNone(diff.getbbox())

        os.remove(generated_meme)


if __name__ == '__main__':
    unittest.main()
