
import pygame as pg
import random
import time
import peice


WIDTH = 400
HEIGHT = 500

BLACK = (0, 0, 0)
GREY = (50, 50, 50)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

FPS = 60
timer = 0
score = 0
t_left = 30
t_right = 30

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Sam's Tetris")
clock = pg.time.Clock()
pg.font.init()

bricks = []
boards = []
completed_line = []

bricks_group = pg.sprite.Group()
next_group = pg.sprite.Group()
brick_index = 0

next_piece = random.choice(peice.pieces)
current_brick = random.choice(peice.pieces)
brick = current_brick[brick_index]

ypos = 5
xpos = 0

restock_pause = False # if true the gme with pause for .25 sec while deleting completed row
run = True
down = False # fast if True
right = False # fast is True
left = False # fast if True

class Brick(pg.sprite.Sprite):
    def __init__(self, **kwargs):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = kwargs['x']
        self.rect.y = kwargs['y']
        self.locked = False

    def update(self):
        if self.locked == False:
            self.image.fill(GREY)
        if self.locked:
            self.image.fill(WHITE)



def create_bricks():

    ''' creating bricks '''

    x = 30
    for i in range(12):
        y = 30
        col = []
        for j in range(20):
            b = Brick(x=x, y=y)
            bricks_group.add(b)
            y += 22
            col.append(b)
        x += 22
        bricks.append(col)


def draw_brick():

    ''' updating pieces on screen '''
    for j in range(len(brick[0])):
        for i in range(len(brick)):
            if brick[i][j] == 'x':
                try:
                    bricks[j + ypos][i + xpos].image.fill(WHITE)
                except:
                    break

def next_board():

    ''' creating the next piece board '''

    b = pg.draw.rect(screen, WHITE, [305, 25, 90, 50], 1)
    margin1 = (90 - (len(next_piece[0][0]) * 10)) / 2
    margin2 = (96 - (len(next_piece[0]) * 10)) / 2
    x = margin1 + 300
    for i in range(len(next_piece[0][0])):
        y = margin2
        for j in range(len(next_piece[0])):
            if next_piece[0][j][i] == 'x':
                b = pg.draw.rect(screen, WHITE, [x, y, 12, 12])
            y += 13
        x += 13


def restock():

    ''' restocking bricks after deleting completed row '''

    global completed_line
    for l in completed_line:
        for i in reversed(range(12)):
            for j in reversed(range(20)):
                if j < l:
                    try:
                        if bricks[i][j].locked == True:
                            bricks[i][j].locked = False
                            bricks[i][j].image.fill(GREY)
                            bricks[i][j + 1].locked = True
                            bricks[i][j + 1].image.fill(WHITE)
                    except:
                        pass
    completed_line = []

def check_row():

    ''' checking completed row '''

    global restock_pause, completed_line, score, down
    completed_line = []
    for i in range(len(bricks[0])): # in range of 20
        hole = 0
        for j in range(len(bricks)): # in range of 12
            ####### if there is a blank brick in a row, add one to hole
            if bricks[j][i].locked == False:
                hole += 1
        ###### if there is row with no blank brick, or if ther is completed row
        if hole == 0:
            completed_line.append(i)

    # deleting completed line
    if len(completed_line) > 0:
        restock_pause = True
        for l in completed_line:
            score += 1
            for m in range(12):
                bricks[m][l].locked = False
                bricks[m][l].image.fill(RED)
        down = False



def bottom_bound():

        ''' checking if the piece is inbound '''

        global xpos, ypos, current_brick, brick, next_piece, run
        bound = 0
        for i in range(len(brick)):
            for j in range(len(brick[0])):
                ####### try to avoid wrong bricks list indexing while mapping elements on its next row
                try:
                    ######## if the piece is at the very bottom of the screen, there is one bound
                    if i + xpos >=19 :
                        bound += 1
                    ######## if the piece is at the top of another piece, there is one bound
                    if bricks[j + ypos][i + xpos + 1].locked == True and brick[i][j] == 'x':
                        bound += 1
                except:
                    break

        if bound == 0:
            # if there is no bound at the bottom, redraw the position of the piece
            draw_brick()

        else:
            ##########
            # checking if the screen is full
            for i in range(12):
                if bricks[i][1].locked:
                    run = False
            ###########


            ###########
            # making the piece locked at its position
            for j in range(len(brick[0])):
                for i in range(len(brick)):
                    if brick[i][j] == 'x':
                        try:
                            bricks[j + ypos][i + xpos].image.fill(WHITE)
                            bricks[j + ypos][i + xpos].locked = True
                        except:
                            pass
            ############

            check_row()  # check if there are completed rows


            ########### bringing the piece position at the top
            xpos = -1
            ypos = 5
            ########### generate new piece
            current_brick = next_piece
            brick = current_brick[0]
            ########### generate next piece
            next_piece = random.choice(peice.pieces)




def left_bound():

    ''' checking if left is bound '''

    bound = False
    for j in range(len(brick[0])):
        for i in range(len(brick)):
            if bricks[j + ypos - 1][i + xpos].locked == True and brick[i][j] == 'x':
                bound = True
    return bound


def right_bound():

    ''' checking if right is bound '''

    bound = False
    for j in range(len(brick[0])):
        for i in range(len(brick)):
            try:
                if bricks[j + ypos + 1][i + xpos].locked == True and brick[i][j] == 'x':
                    bound = True
            except:
                pass
    return bound



def update_game():

    ''' updating the game every second '''

    global xpos, timer
    for i in range(len(bricks)):
        for j in range(len(bricks[0])):
            bricks[i][j].update()

    bottom_bound()
    xpos += 1
    timer = 0


def text_blit():

    ''' blit all the text '''

    myfont1 = pg.font.SysFont('Roboto', 40)
    myfont2 = pg.font.SysFont('Roboto', 25)

    next_font = myfont2.render('Next', True, WHITE)
    score_int = myfont1.render(str(score), True, WHITE)
    center1 = score_int.get_rect(center=(345, 150))
    score_lbl = myfont2.render("score", True, WHITE)
    screen.blit(next_font, (327, 80))
    screen.blit(score_int, center1)
    screen.blit(score_lbl, (326, 180))


def frame():

    ''' making a frame '''

    pg.draw.rect(screen, RED, [25, 25, 273, 448], 5)


create_bricks()


while run:
    clock.tick(FPS)
    screen.fill(BLACK)
    bricks_group.draw(screen)
    next_board()
    text_blit()
    frame()

    if timer >= 30:

        if restock_pause == True:
            restock()
            restock_pause = False
        if restock_pause == False:
            update_game()

    if down:
        timer += 16
    else:
        timer += 1


    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                if not left_bound():
                    if ypos > 0:
                        ypos -= 1
            elif event.key == pg.K_RIGHT:
                if ypos + len(brick[0]) < 12:
                    if not right_bound():
                        ypos += 1
            elif event.key == pg.K_UP:
                try:
                    brick_index += 1
                    brick = current_brick[brick_index]
                except:
                    brick = current_brick[0]
                    brick_index = 0
            elif event.key == pg.K_DOWN:
                down = True
        elif event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                down = False
         
