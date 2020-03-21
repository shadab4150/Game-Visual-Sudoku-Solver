import pygame
import math
import numpy as np
class Sudoku():
    def __init__(self):
        self.W,self.H = (600,600)
        pygame.init()
        pygame.mixer.quit()
        self.screen = pygame.display.set_mode((self.W+200,self.H))
        pygame.display.set_caption("Sudoku Solver")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.focused = None
        self.solve = Button((0,140,0),650,200,100,50,"Solve")
        self.solver = Solver(self.board.sudoku)
        self.run()

    ### Takes care of pygame events from mouse and keyboard     
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.MOUSEBUTTONUP:
                self.focused = self.getCellFromMousePos(pygame.mouse.get_pos())

                if self.solve.isOver(pygame.mouse.get_pos()):
                    self.solver.solve()

            if event.type == pygame.KEYDOWN:
                print("key")
                if self.focused!=None:
                    try:
                        self.board.set_value(self.focused[0],self.focused[1],int(event.unicode))
                    except:
                        pass
    ## Calls paint functions from working units (button, board)
    def paint(self):
        self.screen.fill((255,229,204))
        self.board.paint(self.screen,self.W,self.H)
        self.solve.draw(self.screen)
        pygame.display.flip()
    ## Main loop
    def run(self):
        self.running = True

        while self.running:
            self.dt = self.clock.tick(60)/1000
            self.update()
    ## Update called from main loop
    def update(self):
        self.events()
        self.paint()
    ## Set value on board (Unused)
    def set_value(self,row,col,value):
        self.board.set_value(row,col,value)
    ## Get a cell (0-9,0-9) from the mouse position.
    def getCellFromMousePos(self,coord):
        return (math.floor(coord[0]/(self.W/9)),math.floor(coord[1]/(self.H/9)))


class Board():
    def __init__(self):
        self.sudoku = [ [0]*9 for _ in range(9) ]
        self.font = pygame.font.SysFont('comicsans',81)
    ## Takes a preset board as input - NOT USED
    def set_preset(self,board):
        if len(board)==9 and len(board[1])==9:
            for row in board:
                for cell in row:
                    if board[row][cell]>9 or board[row][cell]<0:
                        return None

            self.sudoku = board
    ## Sets value in a cell
    def set_value(self,row,col,value):
        if self.value_is_valid(value):
            self.sudoku[row][col] = value

    ## Check if an value is valid
    def value_is_valid(self,value):
        if int(value)<=9 and int(value)>=0:
            return True
        return False

    ## Paints grid and numbers to pygame.screen
    def paint(self,screen,width,height):
      ## DRAW background board itself:
        for row in range(10):
            k = row*(height/9)
            pygame.draw.line(screen,(0,0,0),(0,k),(width,k))

        for col in range(10):
            k = col*(width/9)
            pygame.draw.line(screen,(0,0,0),(k,0),(k,height))

        ## Draw numbers:
        for r in range(9):
            for c in range(9):
                value = self.sudoku[r][c]
                if value != 0:
                    text = self.font.render(str(value),2,(0,0,0))
                    screen.blit(text,((width/9)*r+(text.get_width()/2),(height/9)*c))

## Just a button.
class Button:
    def __init__(self,color,x,y,width,heigth,text):
        self.x = x
        self.y = y
        self.width = width
        self.heigth = heigth
        self.text = text
        self.color = color

    def draw(self,window):
        pygame.draw.rect(window,self.color,(self.x,self.y,self.width,self.heigth))

        if self.text!="":
            font = pygame.font.SysFont('comicsans',61)
            text = font.render(self.text,2,(0,0,0))
            window.blit(text,(self.x+(self.width/2 - text.get_width()/2), self.y + (self.heigth/2 -text.get_height()/2)))

    def isOver(self,pos):
        if pos[0] > self.x and pos[0]< (self.x+self.width):
            if pos[1]> self.y and pos[1]< self.y+self.heigth:
                return True

        return False
## Solving algorithm
class Solver:
    def __init__(self,board):
        self.sudoku = board


    def valid(self,row,column,value):
        original = self.sudoku[row][column]

        self.sudoku[row][column] = value

        validity = self.duplicates()

        self.sudoku[row][column] = original

        return not validity

    ## Checks if an array contains duplicates
    def arrayContainsDuplicates(self,array):
        if len(array) == len(set(array)):
            return False
        return True
    ## Trims an array from empty spaces (0's)
    def trimarray(self,array):
        trimmed = []
        for cell in array:
            if cell != 0:
                trimmed.append(cell)
        return trimmed
    ## Finds the next empty cell. Used for backtracking.
    def find_empty(self):
        for i in range(len(self.sudoku)):
            for j in range(len(self.sudoku[i])):
                if self.sudoku[i][j] == 0:
                    return (i,j)
        return None
    ## Checks if the board contains any duplicates in rows, blocks and columns.
    def duplicates(self):
        for row in self.sudoku:
            if self.arrayContainsDuplicates(self.trimarray(row)):
                return True
        for col in map(list,zip(*self.sudoku)):
            if self.arrayContainsDuplicates(self.trimarray(col)):
                return True

        blocks=[[self.sudoku[int(m//3)*3+i][(m%3)*3+j] for i in range(3) for j in range(3)] for m in range(9)]

        for block in blocks:
            if self.arrayContainsDuplicates(self.trimarray(block)):
                return True

        return False
    ## Backtrakcing solving algorithm.
    def solve(self):
        find = self.find_empty()

        if not find:
            return True
        else:
            row,col = find
            for i in range(1,10):
                if self.valid(row,col,i):
                    self.sudoku[row][col] = i

                    if self.solve():
                        return True
                    else:
                        self.sudoku[row][col] = 0

s = Sudoku()
