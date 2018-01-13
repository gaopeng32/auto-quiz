from PIL import Image
from PIL import ImageGrab
import struct
import Quartz.CoreGraphics as CG
import pytesseract


start_x = 10
start_y = 120
width = 344
height = 320
q_height = 180

neg_words = ['没有', '不是', '不会', '不包括', '不属于']
aux_words = ['下列', '以下']
opt_aux_word = ['《', '》']


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

def comp_screenshot_run_time():
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


def get_raw_text_from_screen():
    """Take screenshot of question and options parts. 
    Use OCR to recognize text
    """
    region = CG.CGRectMake(start_x, start_y, width, height)
    im = get_screenshot_v2(region=region)
    q_im = im.crop((0, 0, im.width, q_height))
    opt_im = im.crop((0, q_height, im.width/2, im.height))
    # im.save('images/screen_v2.png')
    # q_im.save("images/question.png")
    # opt_im.save("images/options.png")
    # q_im = Image.open("images/question.png")
    # opt_im = Image.open("images/options.png")
    question_raw = pytesseract.image_to_string(q_im,lang='chi_sim')
    options_raw = pytesseract.image_to_string(opt_im,lang='chi_sim')

    return question_raw, options_raw


def parse_question_option(question_raw, options_raw):
    print(question_raw)
    # Question
    question = question_raw.replace("\n", "").replace(" ", "").lstrip(".1234567890")

    # Options
    options = []
    for opt in options_raw.replace(" ", "").split("\n\n"):
        if opt != "" and not opt.isspace():
            if opt.startswith(opt_aux_word[0]):
                opt = opt[1:]
            if opt.endswith(opt_aux_word[1]):
                opt = opt[:-1]
            options.append(opt)
    is_neg = False
    for word in neg_words:
        if word in question:
            is_neg = True
            break
    for word in neg_words + aux_words:
        if word in question:
            question.replace(word, "")

    return question, options, is_neg
