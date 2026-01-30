#IMPORTS
import pygame as pyg
import numpy as np
import random as ran
import time 
pyg.init()


#CONSTANTS+
board = np.array([[0 , 0 , 0 , 0 , 0 , 0],
                  [0 , 0 , 0 , 0 , 0 , 0],
                  [0 , 0 , 0 , 0 , 0 , 0],
                  [0 , 0 , 0 , 0 , 0 , 0],
                  [0 , 0 , 0 , 0 , 0 , 0],
                  [0 , 0 , 0 , 0 , 0 , 0]])


m1 = np.array([[0,0,0],
               [0,0,0],
               [0,0,0]])

m2 = np.array([[0,0,0],
               [0,0,0],
               [0,0,0]])

m3 = np.array([[0,0,0],
               [0,0,0],
               [0,0,0]])

m4 = np.array([[0,0,0],
               [0,0,0],
               [0,0,0]])

computer = 0

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650

MARBLE_SIZE = 40

MATRIX_SIZE = MARBLE_SIZE*6

player = 1
player1_isrotated=False
player2_isrotated=False

font = pyg.font.Font("font\Grand9K Pixel.ttf" , 40)

base_clr = '#F3FF90'
hover_clr = '#16FF00'
#IMAGE/SOUND LOADERS

bg = pyg.image.load('img\game_bg6.png')

rotate_btn_image = pyg.image.load("img\_rotate2.png")
rotate_btn_image = pyg.transform.scale(rotate_btn_image , (70,70))

empty_btn_img = pyg.image.load("img\empty2.png")
empty_btn_img = pyg.transform.scale(empty_btn_img , (MARBLE_SIZE , MARBLE_SIZE))


marble1_img = pyg.image.load("img\marble_1.png")
marble1_img = pyg.transform.scale(marble1_img , (MARBLE_SIZE,MARBLE_SIZE))

marble2_img = pyg.image.load("img\marble_2.png")
marble2_img = pyg.transform.scale(marble2_img , (MARBLE_SIZE,MARBLE_SIZE))

matrix_img =  pyg.image.load("img\matrix.png")
matrix_img = pyg.transform.scale(matrix_img , (MATRIX_SIZE,MATRIX_SIZE))

marble_sfx = pyg.mixer.Sound('SFX\marble.mp3')
board_sfx = pyg.mixer.Sound('SFX\game_board.mp3')
victory_sfx = pyg.mixer.Sound('SFX\game_victory2.mp3')

#FUNCTIONS/CLASSES

def connect_matricies():
    global m1,m2,m3,m4,board
    connect_matrix(m1,board,1)
    connect_matrix(m2,board,2)
    connect_matrix(m3,board,3)
    connect_matrix(m4,board,4)


def connect_matrix(matrix , board,index_matrix):
    addition_i=0
    addition_j=0
    if index_matrix ==2:
        addition_j=3
    elif index_matrix ==3:
        addition_i=3
    elif index_matrix==4:
        addition_i=3
        addition_j=3
    for i in range(3):
        for j in range(3):
            board[i+addition_i][j+addition_j] = matrix[i][j]


def stalemate(matrix):
    count=0
    for i in range(6):
        for j in range(6):
            if matrix[i][j]!=0:
                count+=1
    if count==36:
        return True
    else:
        return False
    

def check_win(matrix):
    
    if check_win_horizontale(matrix,1) or check_win_vertical(matrix,1) or check_win_oblique(matrix,1):
        return 1
    elif check_win_horizontale(matrix,2) or check_win_vertical(matrix,2) or check_win_oblique(matrix,2):
        return 2
    elif stalemate(matrix):
        return 3
    else:
        return 0 


def check_win_horizontale(board,value):
    for i in range(6):
        count_horizontale=0
        for j in range(6):
            if ( board[i][j]==value):
                count_horizontale+=1
                if count_horizontale==5 :
                    return True
            else:  
                count_horizontale=0
    return False


def check_win_vertical(board,value):
    for i in range(6):
        count_vertical=0
        for j in range(6):
            if ( board[j][i]==value):
                count_vertical+=1
                if count_vertical==5 :
                    return True
            else:
                count_vertical=0
    return False



def check_win_oblique(matrix,value):
    #from left to right
    count=0
    for i in range(6):
        j = i
        if matrix[i][j]==value:
            count+=1
            if count==5:
                return True
        else:
            count=0
    #right to left
    count=0
    for i in range(6):
        j=5-i
        if matrix[i][j]==value:
            count+=1
            if count==5:
                return True
        else:
            count=0
    return False


def switch_turn(player):
    if player == 1:
        player = 2
    elif player == 2:
        player = 1    
    return player


def switch_marble(player,button):
    global player1_isrotated , player2_isrotated
    if button.icon== empty_btn_img  :
        if player == 1 and  not player1_isrotated:
            button.icon = marble1_img
            marble_sfx.play()
            player1_isrotated=True
            player2_isrotated=False
            button.isOccupied = True
            
            return True
        elif player == 2 and not player2_isrotated:
            button.icon = marble2_img
            marble_sfx.play()
            player2_isrotated=True 
            player1_isrotated=False
            button.isOccupied = True
            return True
    else:
       return False

        
    
def play_turn(matrix , r ,c, player):
    
    if matrix[r][c] == 0:
        matrix[r][c] = player


def rotate_matrix_gui(matrix_gui , button_list):
    
    matrix_gui.image = pyg.transform.rotate(matrix_gui.image , 90)
    board_sfx.play()

    i1 = button_list[0].icon
    i2 = button_list[1].icon
    i3 = button_list[2].icon
    i4 = button_list[3].icon
    i6 = button_list[5].icon
    i7 = button_list[6].icon
    i8 = button_list[7].icon
    i9 = button_list[8].icon

    button_list[0].icon = i3
    button_list[1].icon = i6
    button_list[2].icon = i9
    button_list[3].icon = i2
    button_list[5].icon = i8
    button_list[6].icon = i1
    button_list[7].icon = i4
    button_list[8].icon = i7
   

def computer_move(level):
    global m1 ,m2 ,m3 ,m4 , board , player , all_marbles ,list1 ,list2 ,list3 ,list4 ,M1 ,M2 ,M3 ,M4 
    row = ran.randint(0,5)
    column = ran.randint(0,5)
    if level ==1:
        if player==2:
            while(all_marbles[row][column].icon != empty_btn_img):
                row = ran.randint(0,5)
                column = ran.randint(0,5)
            switch_marble(player , all_marbles[row][column])#gui marble switch
            if row < 3 and column < 3 :
                 play_turn(m1 , row , column , 2)
                 
            elif row < 3 and column > 2:
                 play_turn(m2 , row , column-3 , 2)
                      
            elif row >2 and column < 3:
                 play_turn(m3 , row-3 , column , 2)
                      
            else:
                 play_turn(m4 , row-3 , column-3,2)

            if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                      win_screen()               

            #rotate button
            random_rotate = ran.randint(0,3)+1
            if random_rotate==1:
                time.sleep(1)
                rotate_matrix_gui(M1 , list1)
                m1 = np.rot90(m1)
                connect_matricies()
                    

            elif random_rotate==2:
                time.sleep(1)
                rotate_matrix_gui(M2 , list2)
                m2 = np.rot90(m2)
                connect_matricies()

            elif random_rotate==3:
                time.sleep(1)
                rotate_matrix_gui(M3 , list3)
                m3 = np.rot90(m3)
                connect_matricies()
                    

            elif random_rotate==4:
                time.sleep(1)
                rotate_matrix_gui(M4 , list4)
                m4 = np.rot90(m4)
                connect_matricies()

            print(board)

            
            if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                win_screen()
                    
            player = switch_turn(player)   
    if level==2:
        #################
        if player==2:
            result = check_comp_win_horizontale()

            if result is not None:
                row,column=result
            else:
                row=ran.randint(0,5)
                column=ran.randint(0,5)

            switch_marble(player , all_marbles[row][column])#gui marble switch
            if row < 3 and column < 3 :
                 play_turn(m1 , row , column , 2)
                 
            elif row < 3 and column > 2:
                 play_turn(m2 , row , column-3 , 2)
                      
            elif row >2 and column < 3:
                 play_turn(m3 , row-3 , column , 2)
                      
            else:
                 play_turn(m4 , row-3 , column-3,2)

            if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                      win_screen()               

            #rotate button
            random_rotate = ran.randint(0,3)+1
            if random_rotate==1:
                time.sleep(1)
                rotate_matrix_gui(M1 , list1)
                m1 = np.rot90(m1)
                connect_matricies()
                    

            elif random_rotate==2:
                time.sleep(1)
                rotate_matrix_gui(M2 , list2)
                m2 = np.rot90(m2)
                connect_matricies()

            elif random_rotate==3:
                time.sleep(1)
                rotate_matrix_gui(M3 , list3)
                m3 = np.rot90(m3)
                connect_matricies()
                    

            elif random_rotate==4:
                time.sleep(1)
                rotate_matrix_gui(M4 , list4)
                m4 = np.rot90(m4)
                connect_matricies()

            print(board)

            
            if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                win_screen()
                    
            player = switch_turn(player)

         
          

def check_comp_win_horizontale():
     global board
     for i in range(6):
          for j in range(6):
               if board[i][j] == 2 and board[i][j+1] == 0 and j<4:
                    return [i,j+1]
               else: check_comp_win_verticale()
     return None    
    
def check_comp_win_horizontale():
     global board
     for i in range(6):
          for j in range(4):
               if board[i][j] == 2 and board[i][j+1] == 0 and j<4:
                    return [i,j+1]
               else: check_comp_win_verticale()
     return None

def check_comp_win_verticale():
     global board
     for i in range(4):
          for j in range(6):
               if board[i][j]== 2 and board[i+1][j] == 0 and i<5:
                    return [i+1,j]
               else:
                    nb1=ran.randint(0,5)
                    nb2=ran.randint(0,5)
                    return[nb1,nb2]    
               


class Button():
    def __init__(self , x, y, img):
        self.x = x
        self.y = y
        self.icon = img
        self.rect = self.icon.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.isOccupied = False


    def draw(self):
        screen.blit(self.icon, (self.rect.x , self.rect.y))

    def isClickable(self):

        pos = pyg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pyg.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True

            if not pyg.mouse.get_pressed()[0] or not self.rect.collidepoint(pos) :
                self.clicked = False

class MenuButton():
    def __init__(self, x, y ,base_colour ,hovering_colour , text_input):
        self.x = x
        self.y = y
        self.font = font
        self.base_colour = base_colour 
        self.hovering_colour =  hovering_colour
        self.text_input = text_input
        self.text = self.font.render(self.text_input , True , self.base_colour)
        self.rect = self.text.get_rect(center =(self.x , self.y))
        self.clicked = False

    def draw(self):
        screen.blit(self.text , self.rect)

    def change_colour(self):        
        pos = pyg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.text = self.font.render(self.text_input, True , self.hovering_colour)
        else:    
            self.text = self.font.render(self.text_input, True , self.base_colour)

    def isClickable(self):

        pos = pyg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pyg.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True

            if not pyg.mouse.get_pressed()[0]:
                self.clicked = False
                    


class Matrix():
    def __init__(self ,x ,y):
        self.x = x
        self.y = y
        self.image = matrix_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x , self.rect.y))


#DISPLAY

screen = pyg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pyg.display.set_caption("Pentago Game")
CLOCK = pyg.time.Clock()
FPS = 30


#Instances

#______________________rotate buttons_______________

r1 = Button(33,150,rotate_btn_image)
r2 = Button(698,150,rotate_btn_image)
r3 = Button(33,440,rotate_btn_image)
r4 = Button(698,440,rotate_btn_image)

#_________________________Matrices_______________

M1 = Matrix(135,60)
M2 = Matrix(425,60)
M3 = Matrix(135,350)
M4 = Matrix(425,350)

#__________________________matrix 1 buttons(matrix buttons are noted by m(number of matrix)_(row)(column) )
m1_11 = Button(155,80 ,empty_btn_img)
m1_12 = Button(235,80 ,empty_btn_img)
m1_13 = Button(315,80 ,empty_btn_img)

m1_21 = Button(155,160 ,empty_btn_img)
m1_22 = Button(235,160 ,empty_btn_img)
m1_23 = Button(315,160 ,empty_btn_img)

m1_31 = Button(155,240 ,empty_btn_img)
m1_32 = Button(235,240 ,empty_btn_img)
m1_33 = Button(315,240 ,empty_btn_img)

list1 = np.array([m1_11 , m1_12 , m1_13 ,m1_21 , m1_22 , m1_23 , m1_31 , m1_32 , m1_33])
#_________________matrix 2 buttons_______________
m2_11 = Button(445,80 ,empty_btn_img)
m2_12 = Button(525,80 ,empty_btn_img)
m2_13 = Button(605,80 ,empty_btn_img)

m2_21 = Button(445,160 ,empty_btn_img)
m2_22 = Button(525,160 ,empty_btn_img)
m2_23 = Button(605,160 ,empty_btn_img)

m2_31 = Button(445,240 ,empty_btn_img)
m2_32 = Button(525,240 ,empty_btn_img)
m2_33 = Button(605,240 ,empty_btn_img)

list2 = np.array([m2_11, m2_12, m2_13, m2_21, m2_22, m2_23, m2_31, m2_32, m2_33])
#_________________matrix 3 buttons_______________
m3_11 = Button(155,370 ,empty_btn_img)
m3_12 = Button(235,370 ,empty_btn_img)
m3_13 = Button(315,370 ,empty_btn_img)

m3_21 = Button(155,450 ,empty_btn_img)
m3_22 = Button(235,450 ,empty_btn_img)
m3_23 = Button(315,450 ,empty_btn_img)

m3_31 = Button(155,530 ,empty_btn_img)
m3_32 = Button(235,530 ,empty_btn_img)
m3_33 = Button(315,530 ,empty_btn_img)

list3 = np.array([m3_11, m3_12, m3_13, m3_21, m3_22, m3_23, m3_31, m3_32, m3_33])

#_________________matrix 4 buttons_______________
m4_11 = Button(445,370 ,empty_btn_img)
m4_12 = Button(525,370 ,empty_btn_img)
m4_13 = Button(605,370 ,empty_btn_img)

m4_21 = Button(445,450 ,empty_btn_img)
m4_22 = Button(525,450 ,empty_btn_img)
m4_23 = Button(605,450 ,empty_btn_img)

m4_31 = Button(445,530 ,empty_btn_img)
m4_32 = Button(525,530 ,empty_btn_img)
m4_33 = Button(605,530 ,empty_btn_img)

list4 = np.array([m4_11, m4_12, m4_13, m4_21, m4_22, m4_23, m4_31, m4_32, m4_33])

all_buttons = [m1_11 , m1_12 , m1_13 ,m1_21 , m1_22 , m1_23 , m1_31 , m1_32 , m1_33 ,m2_11, m2_12, m2_13, m2_21, m2_22, m2_23, m2_31, m2_32, m2_33 ,m3_11, m3_12, m3_13, m3_21, m3_22, m3_23, m3_31, m3_32, m3_33,m4_11, m4_12, m4_13, m4_21, m4_22, m4_23, m4_31, m4_32, m4_33 ,r1,r2,r3,r4]

all_marbles = np.array([[m1_11 , m1_12 , m1_13 , m2_11 , m2_12 , m2_13],
                        [m1_21 , m1_22 , m1_23 , m2_21 , m2_22 , m2_23],
                        [m1_31 , m1_32 , m1_33 , m2_31 , m2_32 , m2_33],
                        [m3_11 , m3_12 , m3_13 , m4_11 , m4_12 , m4_13],
                        [m3_21 , m3_22 , m3_23 , m4_21 , m4_22 , m4_23],
                        [m3_31 , m3_32 , m3_33 , m4_31 , m4_32 , m4_33]])

#GAME LOOPS

def player_vs_player():
    running = True
    while running:
        global player,m1,m2,m3,m4 , board

        if computer == 1:
             computer_move(1)
        if computer == 2:
             computer_move(2)     

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False
                quit()


            elif player == 1 and player1_isrotated==True or player==2 and player2_isrotated==True:
                if r1.clicked == True :
                    rotate_matrix_gui(M1 , list1)
                    m1 = np.rot90(m1)
                    connect_matricies()
                    if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
                    player = switch_turn(player)    
                    
                elif r2.clicked == True:
                    rotate_matrix_gui(M2 , list2)
                    m2 = np.rot90(m2)
                    connect_matricies()
                    if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3: 
                        win_screen()
                    player = switch_turn(player)    

                elif r3.clicked == True:
                    rotate_matrix_gui(M3 , list3)
                    m3 = np.rot90(m3)
                    connect_matricies()
                    if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
                    player = switch_turn(player)    

                elif r4.clicked == True:
                    rotate_matrix_gui(M4 , list4)
                    m4 = np.rot90(m4)
                    connect_matricies()
                    if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
                    player = switch_turn(player)    


    #_____________MARBLE FUNCTIONS____________________

    # matrix 1
            if m1_11.clicked == True: 
                switch_marble(player , m1_11)
                play_turn(m1 ,0, 0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m1_12.clicked == True:  
                switch_marble(player , m1_12)
                play_turn(m1 ,0, 1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m1_13.clicked == True:
                switch_marble(player , m1_13)
                play_turn(m1 ,0, 2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()


            elif m1_21.clicked == True:  
                switch_marble(player , m1_21)
                play_turn(m1 ,1, 0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
            
            elif m1_22.clicked == True:  
                switch_marble(player , m1_22)
                play_turn(m1 ,1, 1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m1_23.clicked == True:  
                switch_marble(player , m1_23)
                play_turn(m1 ,1, 2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()



            elif m1_31.clicked == True:  
                switch_marble(player , m1_31)
                play_turn(m1 ,2, 0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
            
            elif m1_32.clicked == True:
                switch_marble(player , m1_32)
                play_turn(m1 ,2, 1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m1_33.clicked == True:  
                switch_marble(player , m1_33)    
                play_turn(m1 ,2,2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()


    # matrix 2
            elif m2_11.clicked == True: 
                switch_marble(player , m2_11)
                play_turn(m2 ,0,0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
            
            elif m2_12.clicked == True:  
                switch_marble(player , m2_12)
                play_turn(m2,0,1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m2_13.clicked == True:
                switch_marble(player , m2_13)
                play_turn(m2 ,0,2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()



            elif m2_21.clicked == True:  
                switch_marble(player , m2_21)
                play_turn(m2 ,1,0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
            
            elif m2_22.clicked == True:  
                switch_marble(player , m2_22)
                play_turn(m2 ,1,1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m2_23.clicked == True:
                switch_marble(player , m2_23)
                play_turn(m2 ,1,2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()



            elif m2_31.clicked == True:  
                switch_marble(player , m2_31)
                play_turn(m2 ,2,0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
            
            elif m2_32.clicked == True:
                switch_marble(player , m2_32)
                play_turn(m2 ,2,1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m2_33.clicked == True:  
                switch_marble(player , m2_33)
                play_turn(m2 ,2,2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

    # matrix 3
            elif m3_11.clicked == True: 
                switch_marble(player , m3_11)
                play_turn(m3 ,0,0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3: 
                        win_screen()
            
            elif m3_12.clicked == True:  
                switch_marble(player , m3_12)
                play_turn(m3,0,1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m3_13.clicked == True:
                switch_marble(player , m3_13)
                play_turn(m3 ,0,2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()


            elif m3_21.clicked == True:  
                switch_marble(player, m3_21)
                play_turn(m3, 1, 0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m3_22.clicked == True:  
                switch_marble(player, m3_22)
                play_turn(m3, 1, 1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m3_23.clicked == True:  
                switch_marble(player, m3_23)
                play_turn(m3, 1, 2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()


            elif m3_31.clicked == True:  
                switch_marble(player, m3_31)
                play_turn(m3, 2, 0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m3_32.clicked == True:  
                switch_marble(player, m3_32)
                play_turn(m3, 2, 1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m3_33.clicked == True:  
                switch_marble(player, m3_33)
                play_turn(m3, 2, 2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

    # matrix 4
            elif m4_11.clicked == True: 
                switch_marble(player, m4_11)
                play_turn(m4, 0, 0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()
                
            elif m4_12.clicked == True:  
                switch_marble(player, m4_12)
                play_turn(m4, 0, 1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m4_13.clicked == True:
                switch_marble(player, m4_13)
                play_turn(m4, 0, 2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m4_21.clicked == True:  
                switch_marble(player, m4_21)
                play_turn(m4, 1, 0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m4_22.clicked == True:  
                switch_marble(player, m4_22)
                play_turn(m4, 1, 1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m4_23.clicked == True:  
                switch_marble(player, m4_23)
                play_turn(m4, 1, 2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m4_31.clicked == True:  
                switch_marble(player, m4_31)
                play_turn
                (m4, 2, 0, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m4_32.clicked == True:  
                switch_marble(player, m4_32)
                play_turn(m4, 2, 1, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()

            elif m4_33.clicked == True:  
                switch_marble(player, m4_33)
                play_turn(m4, 2, 2, player)
                connect_matricies()
                if check_win(board) == 1 or check_win(board)== 2 or check_win(board) == 3:
                        win_screen()



            
    #________DRAW ELEMENTS_______
        M1.draw()
        M2.draw()
        M3.draw()
        M4.draw()
        for button in all_buttons:
            button.isClickable()
            button.draw()


        pyg.display.update()  
        CLOCK.tick(FPS)
        screen.blit(bg, (0, 0))



def main_menu():
    pvp_btn = MenuButton( 400 , 100 ,base_clr ,hover_clr,"Player vs. Player")
    pvc_btn = MenuButton( 400 , 300 ,base_clr ,hover_clr,"Player vs. Computer")
    quit_btn = MenuButton( 400 , 500 ,base_clr ,'#FF0000',"Quit")
    running = True

    """
    running 
    """

    while running:
        screen.blit(bg, (0, 0))



        for button in [pvp_btn , pvc_btn ,quit_btn]:
            button.change_colour()
            button.draw()
            button.isClickable()



        for event in pyg.event.get():
            if event.type == pyg.QUIT or quit_btn.clicked == True:
                running = False
                quit()    

            elif pvp_btn.clicked == True:
                player_vs_player()
            elif pvc_btn.clicked == True: 
                difficulty_screen()      


        
        pyg.display.update()  
        CLOCK.tick(FPS)



def win_screen():
    global player , board
    print(board)
    if check_win(board) == 3:
         player_text = 'STALEMATE!'
    else:
        victory_sfx.play()     
        player_text = 'Player '+ str(check_win(board)) + ' Won!'


    win_label = MenuButton( 400 , 100 ,base_clr ,hover_clr, player_text)
    quit_btn2 = MenuButton( 400 , 350 ,base_clr ,"#FF0000","Quit")

    running = True
    """

    
    """
    while running:
        screen.blit(bg, (0, 0))

       
        quit_btn2.change_colour()
        quit_btn2.draw()
        quit_btn2.isClickable()
        win_label.draw()



        for event in pyg.event.get():
            if event.type == pyg.QUIT or quit_btn2.clicked == True:
                running = False
                quit()    
    



        pyg.display.update()  
        CLOCK.tick(FPS)




def difficulty_screen():
    global computer

    set_diff_1 = MenuButton( 400 , 100 ,base_clr ,hover_clr, 'Easy')
    set_diff_2 = MenuButton( 400 , 300 ,base_clr ,'#FC7300', 'Hard')
    back_btn =  MenuButton( 400 , 500 ,base_clr ,'#FF0000', 'Back')

    running = True
    while running:
        screen.blit(bg, (0, 0))

        for button in [set_diff_1,set_diff_2,back_btn]:
             button.change_colour()
             button.isClickable()
             button.draw()

        for event in pyg.event.get():
            if event.type == pyg.QUIT :
                running = False
                quit()    

            elif set_diff_1.clicked == True:
                computer = 1
                player_vs_player()
            elif set_diff_2.clicked == True:      
                computer = 2
                player_vs_player()

            elif back_btn.clicked == True:
                 main_menu() 
        pyg.display.update()  
        CLOCK.tick(FPS)




main_menu()