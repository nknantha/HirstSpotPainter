"""
Hirst Spot Painter:
    `Damien Hirst <https://en.wikipedia.org/wiki/Damien_Hirst>`_ is a famous artist for
his dot / spot paintings. The painting contains random colored dots in some order.

This script contains a class HirstSpotPainter. It creates spot paintings in turtle canvas
using given colors/image and display it to user. Also it gives interactive development support.

:URL: https://github.com/nknantha/HirstSpotPainter
:Author: NanthaKumar <https://github.com/nknantha>
:Date: 2021-09-04
"""
__version__ = '0.2'

import turtle
import math
from random import choice, randint
from colorthief import ColorThief
from typing import Sequence, Tuple, Union


class HirstSpotPainter(turtle.Turtle):
    """
    Class for Spot Painting.
    Note: For generating colors from image file it takes some time. For faster working use higher color value.
    """

    COLORTUPLE = Union[str, Tuple[int, int, int]]
    PATTERNS = ('square', 'circle')

    __slots__ = '_screen', '_wsize', '_colors', '_image_file', '_ccount', '_cquality', '_pattern'

    def __init__(self, size: Tuple[int, int] = (500, 500),
                 colors: Sequence[COLORTUPLE] = ('red', 'green', 'blue'),
                 image_file: str = '', color_quality: int = 5, color_count: int = 20,
                 pattern: str = 'square') -> None:
        """
        Creates HirstSpotPainter instance. If the image parameter is given colors
        parameter will not be considered.

        :param size: Takes a integer tuple contains screen width, height. (Default: (500, 500))
        :param colors: Takes RGB color tuples. It follows tkinter color scheme.
                       (Default: ('red', 'blue', 'green'))
        :param image_file: Takes a file with location.
        :param color_quality: Quality of colors extracted from image. 1 means higher color quality.
                              Higher the quality increase the process time on images. (Default: 5)
        :param color_count: Maximum number of colors to be extracted from image. (Default: 20)
        :param pattern: Takes a pattern name. There are 2 types patterns, square and circle.
                        (Default: 'square')
        """
        if color_quality < 1 or color_count < 1:
            raise ValueError('Color quality and count must be greater than 1')

        self._hspscreen: Union[turtle.TurtleScreen, None] = None
        self._image_file = ''
        self._colors = colors
        self._cquality = color_quality
        self._ccount = color_count

        if pattern in self.PATTERNS:
            self._pattern = pattern
        else:
            raise ValueError(f'Pattern should be one of the {self.PATTERNS}')

        self.screen_size(*size)
        self.refresh_image(image_file)
        self._setup_turtle()
        self._paint()

    def __clear(self):
        """
        Clears the current screen and preserve footer.
        """
        self.clear()
        self._set_footer()

    def _build_colors(self) -> None:
        """
        Rebuild the color from image file.
        """
        if self._image_file:
            print('Generating colors from image, please wait sometimes...')
            self._colors = ColorThief(self._image_file).get_palette(self._ccount, self._cquality)

    def _square_pattern(self):
        """
        Paints square pattern.
        """
        # Padding size around the paint.
        PADX = PADY = 50

        # Calculations.
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

    def _circle_pattern(self):
        """
        Paints circle pattern.
        """
        # Padding size.
        PAD = 50
        DOTSIZE = 15
        STEPSIZE = 25

        # Calculations.
        min_size = self._wsize[0] if self._wsize[0] < self._wsize[1] else self._wsize[1]
        cir_counts = ((min_size // 2) - PAD) // STEPSIZE
        startx, starty = 0, 5

        # Painting dots.
        self.up()
        self.goto(startx, starty)
        self.dot(DOTSIZE, self._yield_color())
        for i in range(cir_counts):
            radius = STEPSIZE + (STEPSIZE * i)
            self.goto(startx, starty - radius)
            self.setheading(0)
            # self.circle(radius, randint(0, 45))
            dot_counts = math.floor((2 * math.pi * radius) / STEPSIZE)
            deg = 360 / dot_counts

            for j in range(dot_counts):
                self.dot(DOTSIZE, self._yield_color())
                self.circle(radius, deg)

    def _paint(self) -> None:
        """
        Starts paints on the screen.
        """

        if self._pattern == 'square':
            self._square_pattern()
        elif self._pattern == 'circle':
            self._circle_pattern()
        else:
            raise ValueError(f'Invalid pattern {self._pattern!r}')

    def _set_footer(self):
        """
        Sets the screen footer with project link.
        """
        if self._hspscreen:
            self.up()
            self.goto((self._wsize[0] // 2) - 299, -((self._wsize[1] // 2) - 10))
            self.color('blue')
            self.write('https://github.com/nknantha/HirstSpotPainter', font=('Arial', 11, 'italic'))
            self.color('black')
            self.home()

    def _setup_turtle(self) -> None:
        """
        Setup turtle as given parameters.
        """
        if not self._hspscreen:
            super().__init__(visible=False)
            self._hspscreen = self.getscreen()
        self._hspscreen.setup(*self._wsize)
        self._hspscreen.screensize(self._wsize[0] - 30, self._wsize[1] - 30)
        self._hspscreen.tracer(2)
        self.speed(9)
        self._hspscreen.title('Hirst Spot Painting')
        self._hspscreen.colormode(255)
        self._set_footer()

    def _yield_color(self) -> Union[str, COLORTUPLE]:
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
        self.__clear()
        self._paint()

    def change_pattern(self, pattern: str) -> None:
        """
        Changes patters with given pattern.
        Patterns: ('square', 'circle')

        :param pattern: Takes a string which must be one of the patterns.
        """
        if pattern in self.PATTERNS:
            self._pattern = pattern
            self.__clear()
            self._paint()
        else:
            raise NameError(f'{pattern!r} is not defined')

    def finalize(self) -> None:
        """
        Finalize the window so that we can't change after this. Invokes the mainloop of screen.
        """
        if self._hspscreen:
            self._hspscreen.mainloop()

    def screen_size(self, x: int = None, y: int = None) -> Union[None, Tuple[int, int]]:
        """
        Returns current screen size if no arguments are passed. If x, y argument is given, changes the screensize
        and repaint the drawing according to the current size. Size cannot be less than (300, 100).

        :param x: Takes an integer denotes width.
        :param y: Takes an integer denotes height.
        :return: None if changes happen else current size in tuple.
        """
        if isinstance(x, int) and isinstance(y, int):
            if x < 300 or y < 100:
                raise ValueError(f'Minimum value (300, 100), given ({x}, {y})')
            self._wsize = (x, y)
            if self._hspscreen:
                self.__clear()
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
            if self._hspscreen:
                self.__clear()
                self._paint()


if __name__ == '__main__':
    # HirstSpotPainter(size=(600, 600), image_file='Images/Image.jpg').finalize()
    HirstSpotPainter(size=(600, 600), image_file='Images/Image.jpg', pattern='circle').finalize()
