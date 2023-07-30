# Meme Generator

Meme Generator is a web application to dynamically generate random or custom memes.

## Folder Structure

```bash
├── _data
│   ├── DogQuotes
│   │   ├── DogQuotes.csv
│   │   ├── DogQuotes.docx
│   │   ├── DogQuotes.pdf
│   │   ├── DogQuotes.txt
│   ├── fonts
│   ├── photos
│   │   ├── dog
│   ├── SimpleLines
│   │   ├── SimpleLines.csv
│   │   ├── SimpleLines.docx
│   │   ├── SimpleLines.pdf
│   │   ├── SimpleLines.txt
├── MemeEngine
│   ├── __init_.py
│   ├── meme_engine.py
├── QuoteEngine
│   ├── __init_.py
│   ├── csv_ingestor.py
│   ├── docx_ingestor.py
│   ├── ingestor_interface.py
│   ├── ingestor.py
│   ├── quote_model.py
│   ├── pdf_ingestor.py
│   ├── text_ingestor.py
├── templates
│   ├── base.html
│   ├── meme_form.html
│   ├── meme.html
├── requirements.txt

```

## Prerequisites

This project uses Python 3.6.3. Install all dependencies given in the requirements.txt file using pip:

````
pip install -r requirements.txt
````

Download and install the pdftotext command line tool from: https://www.xpdfreader.com/download.html

Here are some tips for installing xpdf on different operating systems:

- For **Mac**, we suggest that you use Homebrew:

  - If you don't already have it, install [use the command provided here to install Homebrew](https://brew.sh/). After installing, read the last few lines that it outputs in your CLI—it may provide additional commands that you can run to add Homebrew to PATH.
  - Once Homebrew is installed, simply run brew install xpdf in the terminal.

- For **Windows**, you'll need to:
  
  - [Download the Windows command-line tools from the xpdf website](https://www.xpdfreader.com/download.html).
  - Unzip the files in a location of your choice.
  - Get the full file path to the folder named bin32 (if you have a 32-bit machine) or bin64 (if you have a 64-bit machine)
  - Add this path to the Path environment variable. This will allow you to use the xpdf command from the command line. If you've never done this before, check out [this Stack Overflow post on how to add a folder to the Path environment variable.](https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho)

- For Linux, you can use Homebrew (as shown above for Mac) or _apt-get to install_ (simply enter _sudo apt-get install -y xpdf_ in your command line interface).

## Roles and Responsibilities of Modules 


- QuoteEngine

| Module        | Description   | Dependencies | Returns|
| ------------- |:-------------|:-----:|:------|
| quote_model.py | This module contains a QuoteModel class. This class encapsulates the body and the author of the meme | None | None |
| csv_ingestor.py | This module contains a CSVIngestor class which inherits from the IngestorInterface. It reads data from a CSV file. | None | QuoteModel|
| text_ingestor.py | This module contains a  TextIngestor class which inherits from the IngestorInterface. It reads data from a Text file. | pandas |QuoteModel |
| docx_ingestor.py | This module contains a DocxIngestor class which inherits from the IngestorInterface. It reads data from a DOCX file. | python-docx |QuoteModel |
| pdf_ingestor.py | This module contains a PDFIngestor class which inherits from the IngestorInterface. It reads data from a PDF file.| subprocess module to call  pdftotext CLI utility |QuoteModel |
| ingestor_interface.py | This module contains a IngestorInterface abstract base class. It verifies if the file type is compatible with the ingestor class. It implements abstract method for parsing the file content (i.e., splitting each row) and outputting it to a Quote object. | None | extenstion of the file |
| ingestor.py | This module contains Ingestor class. This class encapsulates all the ingestors to provide one interface to load any supported file type. | None | results from the required ingestor.|

- MemeEngine

| Module        | Description   | Dependencies | Returns|
| ------------- |:-------------|:-----:|:------|
| meme_engine.py | This module contains a MemeEngine class. This class contains make_meme method that loads a file from disk, transform image by resizing to a maximum width of 500px while maintaining the input aspect ratio and add a caption to an image with a body and author to a random location on the image. | Pillow | output path where the meme is saved|

- meme.py

| Module        | Description   | Dependencies | Returns|
| ------------- |:-------------|:-----:|:------|
| meme.py | This module contains a generate_meme method. It generate a randomly captioned image. The program must be executable from the command line and it takes three OPTIONAL arguments: <ul><li> A string quote body </li><li> A string quote author </li><li> An image path </li></ul> | Pillow | a path to a generated image. If any argument is not defined, a random selection is used.|

- app.py

| Module        | Description   | Dependencies | Returns|
| ------------- |:-------------|:-----:|:------|
| app.py | This module uses Quote Engine module and Meme Generator module. It uses the requests package to fetch an image from a user submitted URL. | flask and requests | flask server that dynamically generates random or custom memes|


## Application

The application can be started by running the following command:

````
export FLASK_APP=app.py
flask run --host 0.0.0.0 --port 3000 --reload
````
## Author

Vanditha Chandrashekar Rao- Developer - [rao208](https://github.com/rao208)

## Acknowledgment
. 
[Udacity](https://www.udacity.com/)

