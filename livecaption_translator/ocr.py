from typing import Union, Tuple
import pytesseract
import pygetwindow as gw
from PIL import ImageGrab


class Ocr:
    def __init__(self, pos: Union[Tuple[int, ...], str] = None,
                 tesseract_cmd: str = r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        if pos is not None:
            if isinstance(pos, str):
                self.get_windows_and_set_region(title=pos)
            elif isinstance(pos, tuple):
                self.set_region(pos)
            else:
                raise TypeError("region must be either a str or a tuple of int")
        else:
            self.title = None
            self.region = None
        try:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        except FileNotFoundError:
            print('Tesseract not found. Please install it or specify the path to the executable.')

    def set_region(self, *args):
        if len(args) == 4 and all(isinstance(arg, int) for arg in args):
            left, top, width, height = args
        elif len(args) == 1 and isinstance(args[0], tuple) and len(args[0]) == 4 and all(isinstance(num, int) for num in args[0]):
            left, top, width, height = args[0]
        else:
            raise TypeError("expects 4 individual int arguments or a single tuple with 4 int elements.")

        self.region = (left, top, left + width, top + height)

    def get_windows_and_set_region(self, title: str = '实时辅助字幕'):
        if isinstance(title, str):
            self.title = title
            window = gw.getWindowsWithTitle(title)[0]
        else:
            raise TypeError("expects a string as the title of the window")
        self.set_region(window.left, window.top, window.width, window.height)

    def get_screenshot(self):
        if self.region:
            if self.title:
                self.get_windows_and_set_region(self.title)
            return ImageGrab.grab(bbox=self.region)
        else:
            return ImageGrab.grab()

    def get_text(self):
        return pytesseract.image_to_string(self.get_screenshot()).strip()

