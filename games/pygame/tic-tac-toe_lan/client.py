
import socket
import threading
import pygame
import sys
from client_side_playground import *

class CLIENT:
    #connections vars
    HEADER = 64
    #your ip address goes here
    HOST = '88.212.37.14'
    PORT = 9090
    ADDR = (HOST,PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MSG = "!DISCONNECT"
    
    #pygame vars
    bg_color= (175,175,175)
    width = 600
    height = 600
    clock = pygame.time.Clock()
    
    #game vars
    pattern = "o"
    running = True
    permission = True
    playground_check = [["0","0","0"],["0","0","0"],["0","0","0"]]
    
    def __init__(self):
        #set up communication
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

        #set up pygame window
        self.screen = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("R_P_S")
        self.screen.fill((50,50,50))
        pygame.display.flip()
        self.playground = PLAYER_SIDE(self.screen,self.width,self.height)
        
    #transform list msg to playground    
    def transfer_to_list(self,arr):
        newArr = []

        for i in arr:    
            if i == "x" or i == "o" or i == "0":
                newArr.append(i)
                
        return [newArr[0:3],newArr[3:6],newArr[6:9]]
    
    def recieve(self):
        #program loop
        while True:
            #receive msg length  
            msg_len = self.client.recv(self.HEADER).decode(self.FORMAT)
            
            if msg_len:
                #receive msg
                msg_len = len(msg_len)
                msg = self.client.recv(msg_len).decode(self.FORMAT)

                if msg[0] == "?":
                    #start game
                    if msg == "?GAMEPOSSIBLE":
                        self.running = True
                        self.playground.draw()
                        
                    elif msg[0:5] == "?LINE":
                        self.playground.draw_line(int(float(msg[5])),int(float(msg[6])),int(float(msg[7])),int(float(msg[8])))
                        
                    elif msg == "?PERMISSION":
                        self.permission = True
                    elif msg == "?NEWGAME":
                        self.playground_check = [["0","0","0"],["0","0","0"],["0","0","0"]]
                        self.screen.fill((50,50,50))
                        self.playground.draw()
                        
                if msg[0] == "!":
                    if len(msg) > 4:
                        msg = msg[1:]
                        msg = list(msg)
                        self.playground_check = self.transfer_to_list(msg)
                        for index,i in enumerate(self.playground_check):
                            for n_index,n in enumerate(i):
                                if n == "x":
                                    self.playground.draw_x(n_index,index)
                                elif n == "o":
                                    self.playground.draw_circle(n_index,index)
                        self.playground.draw()
                        
                    if len(msg) == 2:
                        self.pattern = msg[1]
                        self.playground.draw()
    
    def send_msg(self,msg):
        message = msg.encode(self.FORMAT)
        msg_len = len(msg)
        send_len = str(msg_len).encode(self.FORMAT)
        send_len = b' '*(self.HEADER - len(send_len))
        self.client.send(send_len)
        self.client.send(message)
    
    def run_client(self):
        recieve_thread = threading.Thread(target=self.recieve,daemon=True)
        recieve_thread.start()
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.send_msg(self.DISCONNECT_MSG)
                    pygame.quit()
                    sys.exit() 
            
            if self.running == True:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    x = int(pos[0]/self.playground.width)
                    y = int(pos[1]/self.playground.height)
                    if self.permission and self.playground_check[y][x] == "0":
                        self.send_msg(f"!{y}{x}{self.pattern}")      
                        self.permission = False      
                        
            pygame.display.flip()

client = CLIENT()
client.run_client()