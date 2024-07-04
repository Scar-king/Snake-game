import random 
import pygame
import tkinter as tk 
from tkinter import messagebox
pygame.font.init()
pygame.mixer.init()

class cube(object):
    rows = 20
    w = 800
    def __init__(self, start, dirnX = 1, dirnY = 0, color = (255,255,255)):
        self.pos = start
        self.dirnX = dirnX
        self.dirnY = dirnY
        self.color = color

    def move(self, dirnX, dirnY):
        self.dirnX = dirnX
        self.dirnY = dirnY
        self.pos = (self.pos[0] + self.dirnX, self.pos[1] + self.dirnY)

    def draw(self, surface, eyes = False):
        dis = self.w // self.rows
        i = self.pos[0] # i = row
        j = self.pos[1] # j = c

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))
        if eyes: 
            centre = dis // 2
            radius = 3
            circleMiddle = (i*dis+centre-radius, j*dis+8)
            circleMiddle2 = (i*dis + dis-radius*2, j*dis+8)
            pygame.draw.circle(surface, (255,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (255,0,0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnX = 0
        self.dirnY = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnX = -1
                    self.dirnY = 0
                    self.turns[self.head.pos[:]] = [self.dirnX, self.dirnY]
                
                elif keys[pygame.K_RIGHT]:
                    self.dirnX = 1
                    self.dirnY = 0
                    self.turns[self.head.pos[:]] = [self.dirnX, self.dirnY]

                elif keys[pygame.K_UP]:
                    self.dirnX = 0
                    self.dirnY = -1
                    self.turns[self.head.pos[:]] = [self.dirnX, self.dirnY]

                elif keys[pygame.K_DOWN]:
                    self.dirnX = 0
                    self.dirnY = 1
                    self.turns[self.head.pos[:]] = [self.dirnX, self.dirnY]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)

            else : 
#simple mode
                if c.dirnX == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnX == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirnY == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.dirnY == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows-1)

#wall mode
                # if c.dirnX == -1 and c.pos[0] <= 0: (c.rows-1, c.pos[1])
                # elif c.dirnX == 1 and c.pos[0] >= c.rows-1: (0,c.pos[1])
                # elif c.dirnY == 1 and c.pos[1] >= c.rows-1: (c.pos[0], 0)
                # elif c.dirnY == -1 and c.pos[1] <= 0: (c.pos[0], c.rows-1)

                else: c.move(c.dirnX, c.dirnY)
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnX = 0
        self.dirnY = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnX, tail.dirnY

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == 1: 
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

        self.body[-1].dirnX = dx
        self.body[-1].dirnY = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)

def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,0), (x,0), (x,w))
        pygame.draw.line(surface, (255,255,0), (0,y), (w,y))

def DrawScore(surface, score):
    Font = pygame.font.SysFont('Timenewromance', 50)
    Text1 = Font.render('Highest Score: 100', True, (0,0,0))
    Text = Font.render('Score: '+str(score), True, (0,0,0))
    Text2 = Font.render('Play name: Scar King', True, (0,0,0))
    surface.blit(Text1, (10,10))
    surface.blit(Text, (10,50))
    surface.blit(Text2, (10,90))


def redrawWindow(surface):
    global rows, width , s, snack
    surface.fill((255,255,0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    DrawScore(surface, len(s.body)-1)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else: 
            break

    color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    return (x,y), color


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main():
    global width, rows, s, snack
    width = 800
    rows = 20 
    win = pygame.display.set_mode((width, width))
    s = snake((0,0,0), (10,10)) #(10,10) points that snake start
    # snack = cube(randomSnack(rows, s), color = (0,0,0))

    pygame.mixer.music.load('song.mp3')
    pygame.mixer.music.play(-1)
    ate = pygame.mixer.Sound('ok.mp3')
    end = pygame.mixer.Sound('gta.mp3')
    snack_pos, snack_color = randomSnack(rows, s)
    snack = cube(snack_pos, color = snack_color)
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(100)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            ate.play()
            s.addCube()
            snack_pos, snack_color = randomSnack(rows, s)
            snack = cube(snack_pos, color = snack_color)

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                pygame.mixer.music.stop()
                end.play()
                score = len(s.body)
                if score < 10:
                    message_box('You Lost!', f'Score: {len(s.body)} Nice try please try again next time...')
                    s.reset((10,10))
                else:
                    message_box('You Lost!', f'Score: {len(s.body)} you so amazing!')
                    s.reset((10,10))

        redrawWindow(win)
    pass

main()