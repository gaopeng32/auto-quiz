# Python script for automatic question-answer search


## Prerequisite:

* tesseract-ocr with chi-sim language
* python 3.6
	* PIL
	* pytesseract
	* webbrowser
* pytesseract package

In my local environment, I install tesseract-ocr using Homebrew
	```bash
	brew link libtiff
	brew link libpng
	brew link jpeg
	brew install tesseract --with-all-languages
	```
I then create a conda environment and install the python packages
	```bash
	conda create -n autoqa python=3.6 anaconda
	source activate autoqa
	pip install pytesseract
	```


## Usage Guidelines:

My own environment: iphone7 & MacBook Pro 15-inch

1. Start Airserver or equivalent solutions for screen mirroring. Move the mirror screen of iphone to the upper left corner of Mac screen.

2. Activate conda environment: `source activate autoQuiz`

3. Run the script
	```bash
	python ans.py
	```
