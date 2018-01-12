# coding=utf-8

import os
import time
from PIL import Image
from PIL import ImageGrab
# import struct
# import Quartz.CoreGraphics as CG
import pytesseract
import webbrowser
# import subprocess
 
 
class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """

    def capture(self, region = None):
        """region should be a CGRect, something like:
        >>> import Quartz.CoreGraphics as CG
        >>> region = CG.CGRectMake(0, 0, 100, 100)
        >>> sp = ScreenPixel()
        >>> sp.capture(region=region)
        The default region is CG.CGRectInfinite (captures the full screen)
        """

        if region is None:
            region = CG.CGRectInfinite
        else:
            # TODO: Odd widths cause the image to warp. This is likely
            # caused by offset calculation in ScreenPixel.pixel, and
            # could could modified to allow odd-widths
            if region.size.width % 2 > 0:
                emsg = "Capture region width should be even (was %s)" % (
                    region.size.width)
                raise ValueError(emsg)

        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)

        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(prov)

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
    sp = ScreenPixel()
    sp.capture(region=region)
    img = Image.frombytes("RGBA", (sp.width, sp.height), sp._data)
    b, g, r, a = img.split()
    img = Image.merge("RGBA", (r, g, b, a))
    return img


def get_screenshot_v2(region=None):
    img = ImageGrab.grab(bbox=region)
    return img

def main():
    # Record starttime
    start = time.time()

    # region = CG.CGRectMake(0, 100, 380, 550)
    # img = get_screenshot_v1(region=region)

    region = (30,200,580,400)
    img = get_screenshot_2(region=region)
    # img.save("screen.png")

    # OCR text recognition    
    # text=pytesseract.image_to_string(Image.open('screen.png'),lang='chi_sim')
    text = pytesseract.image_to_string(img,lang='chi_sim')
    text =''.join(text.split(" "))
    # print(text)

    # Create Baidu URL and visit
    url = 'http://www.baidu.com/s?wd=%s' % text
    # print(url)

    # subprocess.call(["open", url])
    web = webbrowser.get("chrome") # Need to have this line in Mac OS
    web.open(url)

    # Record endtime
    end = time.time()
    print(end-start)



    #  # Timer helper-function
    # import contextlib
 
    # @contextlib.contextmanager
    # def timer(msg):
    #     start = time.time()
    #     yield
    #     end = time.time()
    #     print ("%s: %.02fms" % (msg, (end-start)*1000))
 
    # # # Example usage
    # # sp = ScreenPixel()
 
    # with timer("Capture"):
    #     # Take screenshot
    #     region = CG.CGRectMake(0, 0, 1000, 1000)
    #     # region = None
    #     img = get_screenshot(region=region)
 
    # with timer("Save"):
    #     img.save("test.png")

 

if __name__ == "__main__":
    main()

