import random, pygame, sys
from pygame.locals import *
import datetime
from os import listdir, path
from os.path import isfile, join
from dateutil import relativedelta

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--directory", help="full directory path of the clips you want to use")
args = parser.parse_args()

FPS = 30  # frames per second, the general speed of the program
REVEAL_TIME_IN_SECONDS = 30
WINDOWWIDTH = 1200  # size of window's width in pixels
WINDOWHEIGHT = int(WINDOWWIDTH * 9 / 16)  # size of windows' height in pixels

if args.directory:
    if path.isdir(args.directory):
        PIC_FOLDER = args.directory
    else:
        raise Exception(f'the provided directory path = {args.directory} is not valid')
else:
    # noting provided, lets use the example directory
    dir, file = path.split(__file__)
    PIC_FOLDER = path.join(dir, 'example_quiz')

#            R    G    B
GRAY = (100, 100, 100)
NAVYBLUE = (60, 60, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)


class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class Square:

    def __init__(self, rect: pygame.Rect):
        self.rect: pygame.Rect = rect
        self.reveal_point: float = 0

    def draw(self, screen):
        pygame.draw.rect(DISPLAYSURF, GREEN, self.rect)

    def is_hidden(self, progress: float):
        return progress < self.reveal_point


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    GAME_AREA = pygame.Rect(0, 50, WINDOWWIDTH, WINDOWHEIGHT - 50)

    n_rows = 10
    n_columns = 10

    src_pics = [f for f in listdir(PIC_FOLDER) if isfile(join(PIC_FOLDER, f))]

    i_pic = 0
    scaled_picture, scaled_picture_rect, squares = set_up_image(GAME_AREA,
                                                                n_columns,
                                                                n_rows,
                                                                src_pics,
                                                                i_pic)

    start_reveal_button = Button(WHITE, 5, 5, 300, 40, "Start Reveal")
    next_item_button = Button(WHITE, 310, 5, 140, 40, "Next")
    prev_item_button = Button(WHITE, 455, 5, 140, 40, "Prev")
    full_reveal_button = Button(WHITE, 600, 5, 300, 40, "Full Reveal")

    start_time = None
    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_reveal_button.is_over(pos):
                    start_time = datetime.datetime.now()

                elif full_reveal_button.is_over((pos)):
                    start_time = datetime.datetime.now() - relativedelta.relativedelta(seconds=REVEAL_TIME_IN_SECONDS)

                elif next_item_button.is_over(pos) or prev_item_button.is_over(pos):
                    if next_item_button.is_over(pos):
                        i_pic = i_pic + 1
                        if i_pic >= len(src_pics):
                            i_pic = 0
                    else:
                        i_pic = i_pic - 1
                        if i_pic < 0:
                            i_pic = len(src_pics) - 1

                    scaled_picture, scaled_picture_rect, squares = set_up_image(GAME_AREA,
                                                                                n_columns,
                                                                                n_rows,
                                                                                src_pics,
                                                                                i_pic)
                    start_time = None

        if start_time is not None:
            progress = (datetime.datetime.now() - start_time).total_seconds() / REVEAL_TIME_IN_SECONDS
        else:
            progress = 0

        # now draw the screen
        pygame.display.set_caption(f'Film & TV Quiz - Reveal Picture Question {i_pic + 1}')

        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(scaled_picture, scaled_picture_rect)
        start_reveal_button.draw(DISPLAYSURF)
        next_item_button.draw(DISPLAYSURF)
        prev_item_button.draw(DISPLAYSURF)
        full_reveal_button.draw(DISPLAYSURF)

        for square in squares:
            if square.is_hidden(progress):
                pygame.draw.rect(DISPLAYSURF, GREEN, square.rect)

        pygame.display.flip()
        FPSCLOCK.tick(FPS)


def set_up_image(GAME_AREA, n_columns, n_rows, picture_files, i_pic):
    # scale to fit
    raw_picture = pygame.image.load(join(PIC_FOLDER, picture_files[i_pic]))
    game_ratio = GAME_AREA.size[0] / GAME_AREA.size[1]
    picture_ratio = raw_picture.get_rect().size[0] / raw_picture.get_rect().size[1]

    if picture_ratio < game_ratio:
        height = GAME_AREA.size[1]
        scaled_picture = pygame.transform.scale(raw_picture, (int(height * picture_ratio), height))
    else:
        width = GAME_AREA.size[0]
        scaled_picture = pygame.transform.scale(raw_picture, (width, int(width / picture_ratio)))

    scaled_picture_rect = scaled_picture.get_rect().move(*GAME_AREA.topleft)
    square_width = int(scaled_picture_rect.size[0] / n_rows)
    square_height = int(scaled_picture_rect.size[1] / n_columns)

    squares: list[Square] = []
    x_start = scaled_picture_rect.left
    for i in range(0, n_rows):
        x_end = x_start + square_width
        y_start = scaled_picture_rect.top
        for j in range(0, n_columns):
            y_end = y_start + square_height
            squares.append(Square(pygame.Rect((x_start, y_start), (square_width, square_height))))
            y_start = y_end + 1
        x_start = x_end + 1
    # put into random order
    random.shuffle(squares)
    for i, square in enumerate(squares):
        square.reveal_point = (i + 1) / len(squares)
    return scaled_picture, scaled_picture_rect, squares


if __name__ == '__main__':
    main()
