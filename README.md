# A Python tool for automatic question-answer search


## Prerequisite:

* tesseract-ocr with chi-sim language
* python 3.6
	* PIL
	* pytesseract
	* webbrowser
* pytesseract package

In my local environment, I installed the tesseract-ocr using Homebrew

```bash
brew link libtiff
brew link libpng
brew link jpeg
brew install tesseract --with-all-languages
```

I then created a conda environment and installed the python packages

```bash
conda create -n autoquiz python=3.6 anaconda
source activate autoquiz
pip install pytesseract
```


## Usage Guidelines:

My own environment: iphone7 & MacBook Pro 15-inch

1. Start Airserver or equivalent solutions for screen mirroring. Move the mirror screen of iphone to the upper left corner of Mac screen.

2. Activate conda environment: 

```bash
source activate autoquiz
```

3. Run the script
	
```bash
python ans_v1.py
python ans_v2.py
```


## Contact
Peng Gao, <gaopeng32@gmail.com>

For voice search solutions, it is worth to try [Baidu searchcraft](http://secr.baidu.com/).