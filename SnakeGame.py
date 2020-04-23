# Snake Game created by Kerry Liu

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# cube object class
class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        # initiate all the parameters
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)  # update the position

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows  # get the distance between each line
        i = self.pos[0]  # row
        j = self.pos[1]  # column

        # draw the cube , +1 and -2 is used to show the white lines of the grid
        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:  # draw the eyes
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


# snake object class contains the cube object
class snake(object):
    body = []  # list of cubes
    turns = {}

    def __init__(self, color, pos):  # define all the parameters that passed in
        self.color = color
        self.head = cube(pos)  # head has the position that passed in
        self.body.append(self.head)
        # since the snake can only move in one direction, so the x and y direction must be one 0 and one 1
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # if the user click the exit, it will exit the game
                pygame.quit()

            keys = pygame.key.get_pressed()  # get all the key values

            for key in keys:
                if keys[pygame.K_a]:  # if the a button is pressed, go left
                    self.dirnx = -1
                    self.dirny = 0
                    # set the current head direction to the new turned direction
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_d]:  # if the d button is pressed, go right
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_w]:  # if the w button is pressed, go up
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_s]:  # if the a button is pressed, go down
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):  # get the index and cube of the body, iterate through the list of the position
            p = c.pos[:]  # grab the c position
            if p in self.turns:  # if the position is in the turns, then turn
                turn = self.turns[p]  # the actual turn is equal to the turn at the index
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:  # if it is not in the list
                if c.dirnx == -1 and c.pos[0] <= 0:  # check if it is going off the screen from the left
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:  # check if it is going off the screen from the right
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:  # check if it is going off the screen from the down
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:  # check if it is going off the screen from the up
                    c.pos = (c.pos[0], c.rows - 1)
                else:  # if none of is true
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)  # setting a new head
        self.body = []  # clearing the class variable
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]  # the last element in the list
        dx, dy = tail.dirnx, tail.dirny

        # check which direction is the snake moving
        if dx == 1 and dy == 0:  # if the snake is moving right
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:  # if the snake is moving left
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:  # if the snake is moving down
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:  # if the snake is moving up
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        # changing the cube direction with the direction of the snake tail
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:  # if it is the head, true for the eyes
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows  # find the size between the lines

    x = 0  # initialize the x and y value at the top corner
    y = 0
    for l in range(rows):  # iterate through the window to draw the horizontal and vertical lines
        x = x + sizeBtwn  # increase by size between each time
        y = y + sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))  # draw the vertical lines  Start position (x, 0)
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))  # draw the horizontal lines  Start position (0, y)


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0, 0, 0))  # fill the screen with black background
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)  # draw the grid on the window
    pygame.display.update()  # update the window


def randomSnack(rows, item):
    positions = item.body  # set a new list to the body list

    while True:
        x = random.randrange(rows)  # randomly get a x position
        y = random.randrange(rows) # randomly get a y position
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:  # a filtered list check if the snack is on top of the snake
            continue  # do this again
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)  # creating a window on to p of everything
    root.withdraw()
    messagebox.showinfo(subject, content)  # shows information passed in
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 500  # set the width and height
    rows = 20  # set the number of rows
    win = pygame.display.set_mode((width, width))  # create the window of the game
    pygame.init()  # initialize the caption
    pygame.display.set_caption('Snake Game by Kerry')  # add a caption to the window
    s = snake((255, 0, 0), (10, 10))  # initialize a snake object
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # initiate a snack for the snake
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)  # a delay with 50 milliseconds so the program does not run too fast, lower and faster
        clock.tick(8)  # make sure the game does not run more than 8 frame per second. lower and slower
        s.move()
        if s.body[0].pos == snack.pos:  # if the snake eats a snack then add a cube to the snake body
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))  # generate a new snack

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):  # if the position is in any of the postion after
                print('Score: ', len(s.body))  # print the score to the console
                message_box('You Lost!', 'Play again... Score: {}'.format(len(s.body)))  # display the message box
                pygame.init()  # initialize the caption
                # update the latest score every time
                pygame.display.set_caption('Snake Game by Kerry. Last Game Score: {}'.format(len(s.body)))
                s.reset((10, 10))  # reset the snake position
                break

        redrawWindow(win)  # redraw the window every time

    pass


main()
