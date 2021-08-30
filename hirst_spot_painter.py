"""
Hirst Spot Painter:
    `Damien Hirst <https://en.wikipedia.org/wiki/Damien_Hirst>`_ is a famous artist for
his dot / spot paintings. The painting contains random colored dots in some order.

This script contains a class HirstSpotPainter. It creates spot paintings in turtle canvas
using given colors/image and display it to user. Also it gives interactive development support.

:URL: https://github.com/nknantha/HirstSpotPainter
:Author: NanthaKumar <https://github.com/nknantha>
:Date: 2021-08-30
"""
__version__ = '0.1'

import turtle
from random import choice
from colorthief import ColorThief
from typing import Sequence, Tuple, Union


class HirstSpotPainter(turtle.Turtle):
    """
    Class for Spot Painting.
    Note: For generating colors from image file it takes some time. For faster working use higher color value.
    """

    COLORTUPLE = Union[str, Tuple[int, int, int]]

    __slots__ = '_screen', '_wsize', '_colors', '_image_file', '_ccount', '_cquality', '_speed'

    def __init__(self, size: Tuple[int, int] = (500, 500),
                 colors: Sequence[COLORTUPLE] = ('red', 'blue', 'green'),
                 image_file: str = None, color_quality: int = 5, color_count: int = 20) -> None:
        """
        Creates HirstSpotPainter instance. If the image parameter is given colors
        parameter will not be considered.

        :param size: Takes a integer tuple contains screen width, height. (Default: (500, 500))
        :param colors: Takes RGB color tuples. It follows tkinter color scheme.
                       (Default: ('red', 'blue', 'green'))
        :param image_file: Takes a file with location..
        :param color_quality: Quality of colors extracted from image. 1 means higher color quality.
                              Higher the quality increase the process time on images. (Default: 5)
        :param color_count: Maximum number of colors to be extracted from image. (Default: 20)
        """
        if color_quality < 1 or color_count < 1:
            raise ValueError('Color quality and count must be greater than 1')

        self._screen = None
        self._image_file = None
        self._colors = colors
        self._cquality = color_quality
        self._ccount = color_count

        self.screen_size(*size)
        self.refresh_image(image_file)
        self._setup_turtle()
        self._paint()

    def _build_colors(self) -> None:
        """
        Rebuild the color from image file.
        """
        if self._image_file:
            self._colors = ColorThief(self._image_file).get_palette(self._ccount, self._cquality)

    def _paint(self) -> None:
        """
        Starts create window and paints.
        """
        'https://github.com/nknantha/HirstSpotPainter'
        # Getting configuration.
        PADX = PADY = 50
        startx, starty = -(int(self._wsize[0] / 2) - PADX), -(int(self._wsize[1] / 2) - PADY)
        DOTSIZE = 15
        STEPSIZE = 25
        dotcountx = int(self._wsize[0] - (2 * PADX)) // STEPSIZE
        dotcounty = int(self._wsize[1] - (2 * PADY)) // STEPSIZE

        # Painting dots.
        self.up()
        for i in range(dotcounty + 1):
            self.goto(startx, starty + (STEPSIZE * i))
            self.dot(DOTSIZE, self._yield_color())
            for j in range(dotcountx):
                self.fd(STEPSIZE)
                self.dot(DOTSIZE, self._yield_color())

    def _setup_turtle(self) -> None:
        """
        Setup turtle as given parameters.
        """
        if not self._screen:
            super().__init__(visible=False)
            self._screen = self.getscreen()
        self._screen.setup(*self._wsize)
        self._screen.tracer(2)
        self._screen.title('Hirst Spot Painting')
        self._screen.colormode(255)

    def _yield_color(self) -> Tuple[int, int, int]:
        """
        Yields color from colors in random manner.
        :return: A color tuple contains RGB values.
        """
        return choice(self._colors)

    def change_colors(self, colors: Sequence[COLORTUPLE]) -> None:
        """
        Changes colors with given colors.
        :param colors: Takes collection of color tuples.
        """
        self._colors = colors
        if self._image_file:
            self._image_file = ''
        self.clear()
        self._paint()

    def finalize(self) -> None:
        """
        Finalize the window so that we can't change after this. Invokes the mainloop of screen.
        """
        if self._screen:
            self._screen.mainloop()

    def screen_size(self, x: int = None, y: int = None) -> Union[None, Tuple[int, int]]:
        """
        Returns current screen size if no arguments are passed. If x, y argument is given, changes the screensize
        and repaint the drawing according to the current size. Size cannot be less than (150, 100).

        :param x: Takes an integer denotes width.
        :param y: Takes an integer denotes height.
        :return: None if changes happen else current size in tuple.
        """
        if isinstance(x, int) and isinstance(y, int):
            if x < 150 or y < 100:
                raise ValueError(f'Minimum value (150, 150), given ({x}, {y})')
            self._wsize = (x, y)
            if self._screen:
                self.clear()
                self._setup_turtle()
                self._paint()
            return None
        return self._wsize

    def refresh_image(self, image_file: str = '') -> None:
        """
        Refresh/reload image and extract color from them. If empty string given it just reload image.
        :param image_file: Takes an image file. (Default: '')
        """
        if image_file:
            self._image_file = image_file
        if self._image_file:
            self._build_colors()
            if self._screen:
                self.clear()
                self._paint()


if __name__ == '__main__':
    # Photo by Steve Johnson from Pexels
    HirstSpotPainter(size=(600, 600), image_file='Images/Image.jpg').finalize()
