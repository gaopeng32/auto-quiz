# coding=utf-8

# Written by Peng Gao (gaopeng32@gmail.com, pgao@princeton.edu) in Jan 2018

import os
import time
from PIL import Image
from PIL import ImageGrab
import struct
import Quartz.CoreGraphics as CG
import pytesseract
import webbrowser
# import subprocess
 
 
class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """

    def capture(self, region = None):
        """capture screenshot from region
        :region: tuple of (x, y, width, height)
        """

        if region is None:
            region = CG.CGRectInfinite # full screen

        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(CG.CGImageGetDataProvider(image))

        # Get width/height of image
        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)

    def pixel(self, x, y):
        """Get pixel value at given (x,y) screen coordinates
        Must call capture first.
        """

        # Pixel data is unsigned char (8bit unsigned integer),
        # and there are for (blue,green,red,alpha)
        data_format = "BBBB"

        # Calculate offset, based on
        # http://www.markj.net/iphone-uiimage-pixel-color/
        offset = 4 * ((self.width*int(round(y))) + int(round(x)))

        # Unpack data from string into Python'y integers
        b, g, r, a = struct.unpack_from(data_format, self._data, offset=offset)

        # Return BGRA as RGBA
        return (r, g, b, a)

def get_screenshot_v1(region=None):
    """Use PIL.ImageGrab to take a screenshot 
    """

    im = ImageGrab.grab(bbox=region)
    return im

def get_screenshot_v2(region=None):
    """Use CoreGraphics to take a screenshot (faster capturing time)
    """

    sp = ScreenPixel()
    sp.capture(region=region)
    im = Image.frombytes("RGBA", (sp.width, sp.height), sp._data, "raw", "BGRA")
    return im


def comp_run_time():
    """Compare the running time of different screenshot methods
    """

    import contextlib
 
    @contextlib.contextmanager
    def timer(msg):
        start = time.time()
        yield
        end = time.time()
        print ("%s: %.02fms" % (msg, (end-start)*1000))
 
    with timer("v1.capture"):
        region = (30,230,700,400)
        im1 = get_screenshot_v1(region=region)

    with timer("v1.save"):
        im1.save("screen_v1.png")

    with timer("v2"):
        region = CG.CGRectMake(10, 120, 344, 80)
        im2 = get_screenshot_v2(region=region)

    with timer("v2.save"):
        im2.save("screen_v2.png")


def main():
    # comp_run_time()

    # Record starttime
    start = time.time()

    # Region for screenshot
    # The values are tuned for iphone7 & MacBook Pro (Retina, 15-inch, Mid 2014)
    
    # v1:
    # region = (30,230,700,400)
    # im = get_screenshot_v1(region=region)

    # v2: 
    region = CG.CGRectMake(10, 120, 344, 80)
    im = get_screenshot_v2(region=region)
    # im.save("screen.png")

    # OCR text recognition    
    text = pytesseract.image_to_string(im,lang='chi_sim')
    text =''.join(text.split(" "))
    # print(text)

    # Create Baidu URL and visit
    url = 'http://www.baidu.com/s?wd=%s' % text
    # print(url)

    web = webbrowser.get("chrome") # need to specify brower code in Mac OS
    web.open(url)
    # subprocess.call(["open", url])

    # Record endtime
    end = time.time()
    print(end-start)

 

if __name__ == "__main__":
    main()

