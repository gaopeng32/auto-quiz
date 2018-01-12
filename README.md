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
conda create -n autoqa python=3.6 anaconda
source activate autoqa
pip install pytesseract
```


## Usage Guidelines:

My own environment: iphone7 & MacBook Pro 15-inch

1. Start Airserver or equivalent solutions for screen mirroring. Move the mirror screen of iphone to the upper left corner of Mac screen.

2. Activate conda environment: 

```bash
source activate autoqa
```

3. Run the script
	
```bash
python ans.py
```

* ```get_screenshot_v1()```: Use PIL.ImageGrab to take a screenshot
* ```get_screenshot_v2()```: Use CoreGraphics to take a screenshot (faster capturing time)


## Contact
Peng Gao, <gaopeng32@gmail.com>, <pgao@princeton.edu>

For voice search solutions, it is worth to try [Baidu searchcraft] (http://secr.baidu.com/).