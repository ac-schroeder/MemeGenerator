# Meme Generator

The Meme Generator is a small web app built in Python with Flask, that uses the Pillow library to combine images and captions to create simple memes. It can also be run from the command line.

It can randomly generate memes, or it can create memes from user-supplied content.

It parses PDF, CSV, DocX, and text files to read quotes for use in the memes. 

It uses the Requests library to download user-supplied images.

This project was developed as part of a python course.


## Setting Up and Running

To run this app, [XpdfReader](https://www.xpdfreader.com/) must be installed, as it runs it as a subprocess. 

To get going, import required libraries from the requirements file:

    pip install -r requirements.txt

To run the web app, set the Flask environment variable and start the server: 
        
    flask run

To run from the command line, use the following syntax:

    To generate a random meme:

        python meme.py

    To supply a custom image and quote:

        python meme.py --path 'sample\path' --body 'sample quote' --author 'sample author'


## The Quote Engine Module

The QuoteEngine module is responsible for parsing different file types to read quotes and compiling them for use by the app. It is called when the app generates a random meme from the default collection of quotes.

The path to the quotes files directory is set in constants.py. The module searches the directory for supported file types to read. For each supported file type, it reads and converts its contents to a list of quotes containing text and author.

The module supports CSV, PDF, DocX, and text files. 

Several libraries are used to handle the different file types:

    - pandas 
    - python-docx
    - subprocess, which calls the external process XpdfReader

If no supported files containing quotes are available at the specified directory, the web app will not support the random meme generation feature, and will only display the form to create a custom meme.


## The Meme Engine Module

The MemeEngine class generates memes based on input quotes and images. Both random and custom meme generation use this class to generate their memes. 

The module makes use of the Pillow library to modify the provided image with the quote as overlaid text.

The MemeEngine class must be initialised with a directory for storing finished memes. The default path to a static output directory is set in constants.py. 

To initialise the MemeEngine class with an output directory, use:

    meme = MemeEngine(output_dir)     

To generate a meme:

    meme.make_meme(img_path, text, author, width)
