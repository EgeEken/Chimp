import pygame as pg
import random
import time

pg.init()

SIZE = 50 # WARNING: IF SIZE IS TOO BIG, THE GAME WILL START TO LAG AND EVENTUALLY CRASH DUE TO THE NUMBER OF BOXES NOT FITTING ON SCREEN, KEEP THE SIZE/SCREENSIZE RATIO BELOW 1/10
SCREENSIZE = 700 # ALSO IF THE SCREEN IS TOO SMALL, REMEMBER, 1/10 RATIO

SHOWN = (140, 140, 220)
EMPTY = (170,170,170)
BACKGROUND = (255,255,255)
FONT = pg.font.SysFont("timesnewroman.ttf", 72)
TEXT = (20, 20, 20)

class Game:
    def __init__(self, size = 50, screensize = 700):
        self.size = size
        self.screen = pg.display.set_mode((screensize, screensize))
        self.screensize = screensize
        self.score = 3 #3 is the starting point
        self.state = "End" #View, Play, End
        self.boxes = dict() #List of boxes youre supposed to click on (int boxnumber: (int, int) position)
        self.shownboxes = {0,1,2} #List of boxes that are shown without numbers on them, remove one when it is clicked (boxnumber)

    def overlapcheck(self, poslist):
        for pos in poslist:
            for pos2 in poslist:
                if pos != pos2:
                    if (pos[0] <= pos2[0] + self.size*2 and pos[0] >= pos2[0] - self.size*2) and (pos[1] <= pos2[1] + self.size*2 and pos[1] >= pos2[1] - self.size*2):
                        return True
        return False

    def generate_boxdict(self):
        self.boxes = dict()
        poslist = [(random.randint(self.size, self.screensize-self.size), random.randint(self.size, self.screensize-self.size)) for i in range(self.score)]
        while self.overlapcheck(poslist):
            poslist = [(random.randint(self.size, self.screensize-self.size), random.randint(self.size, self.screensize-self.size)) for i in range(self.score)]
        for i in range(self.score):
            self.boxes[i] = poslist[i]
        self.shownboxes = {j for j in range(self.score)}
        
    def update(self):
        self.screen.fill(EMPTY)
        if self.state == "View":
            for box in self.boxes:
                pg.draw.rect(self.screen, SHOWN, (self.boxes[box][0]-self.size, self.boxes[box][1]-self.size, self.size*2, self.size*2))
                text = FONT.render(str(box + 1), True, TEXT)
                self.screen.blit(text, (self.boxes[box][0]-text.get_width()//2, self.boxes[box][1]-text.get_height()//2))
        elif self.state == "Play":
            for box in self.shownboxes:
                pg.draw.rect(self.screen, SHOWN, (self.boxes[box][0]-self.size, self.boxes[box][1]-self.size, self.size*2, self.size*2))
        pg.display.update()

    def mousepostobox(self, pos):
        x, y = pos
        if x > self.screensize or x < 0 or y < 0 or y > self.screensize:
            return None
        for box in self.boxes:
            if self.boxes[box][0]-self.size <= x and x <= self.boxes[box][0]+self.size and self.boxes[box][1]-self.size <= y and y <= self.boxes[box][1]+self.size:
                return box
        return None

    def play(self):
        self.score = 3
        self.shownboxes = {0,1,2}
        while self.state != "End":
            self.boxes = dict()
            self.update()
            time.sleep(0.1)
            self.generate_boxdict()
            self.update()
            self.state = "Play"
            while self.state == "Play":
                for event in pg.event.get():
                    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                        pg.quit()
                    elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        lastclick = self.mousepostobox(pg.mouse.get_pos())
                        if lastclick != None and lastclick in self.shownboxes:
                            if lastclick == len(self.boxes) - len(self.shownboxes):
                                self.shownboxes.remove(len(self.boxes) - len(self.shownboxes))
                                self.update()
                                if len(self.shownboxes) == 0:
                                    self.score += 1
                                    self.update()
                                    self.state = "View"
                            else:
                                self.state = "End"
                    pg.event.clear(pg.MOUSEBUTTONDOWN)

    def menu(self):
        self.screen.fill(BACKGROUND)
        pressspace = FONT.render("Press space to play", True, TEXT)
        if self.score > 3:
            scorecount = FONT.render(f'Score: {self.score - 1}', True, TEXT)
            self.screen.blit(scorecount, (10, 10))
        self.screen.blit(pressspace, (10, 10 + pressspace.get_height()))
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.state = "View"

    def run(self):
        while True:
            if self.state == "View" or self.state == "Play":
                self.play()
            elif self.state == "End":
                self.menu()
                

def main():
    game = Game(SIZE, SCREENSIZE)
    game.run()


if __name__ == "__main__":
    main()
