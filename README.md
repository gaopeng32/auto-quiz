# Simple python script for automatic question search

## Prerequisite:

* python 3.6
* tesseract package with chi-sim
	* brew link libtiff 
	* brew link libpng 
	* brew link jpeg
	* brew install tesseract --with-all-languages
* pytesseract package
	* pip install pytesseract

In my local environment, I create a conda environment for this.
	* conda create -n autoQuiz python=3.6 anaconda



## Usage:

* Start AirServer for Mac & screen mirroring. Move the mirror screen to the upper left corner
* source activate autoQuiz
* cd autoQuiz
* python ans_v1.py