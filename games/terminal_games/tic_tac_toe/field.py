from vars import *
from random import random as rdm

class Game:
    def __init__(self,play_field,game_mode="bot",first_player="You",second_player="bot") -> None:
        
        self.play_field = play_field
        self.pos_of_items = [[0,0,0],[0,0,0],[0,0,0]]
        self.game_mode = game_mode
        self.first_player = first_player
        self.second_player = second_player
        self.player_score = {"first_player":0,"second_player":0}
        self.position_of_input_fields = [[0, 0], [0, 2], [0, 4], [2, 0], [2, 2], [2, 4], [4, 0], [4, 2], [4, 4]]
        self.player = "o"
        self.running = True
        
        self.draw()
        
    def draw(self):
        for row in self.play_field:
            print(row[0])
    
    def names(self):
        if self.player == "x":
            return self.first_player
        else:
            return self.second_player
    
    def easy_bot(self):
        return int(rdm()*9)
    
    def player_mode_logic(self,player_name):
        position_of_input = input("What would be player "+player_name+" with "+self.player+" next move (select option from 1 to 9): ")
        try:
            position_of_input = int(position_of_input)
            return position_of_input
        except:
            self.player_turn()
            return

    def player_turn(self):
        player_name = self.names()
        
        if self.game_mode == 'player':    
            position_of_input = self.player_mode_logic(player_name)
            
        else:
            if player_name == "bot":
                position_of_input = self.easy_bot()
            else:
                position_of_input = self.player_mode_logic(player_name)
    
        if position_of_input >= 1 and position_of_input <=9:
            position_of_input -= 1
            if self.pos_of_items[cases[position_of_input][0]][cases[position_of_input][1]] == 0:
                pos = self.position_of_input_fields[position_of_input]
                string =  self.play_field[pos[0]]
                proccesing_str = list(string[0])
                proccesing_str[pos[1]] = self.player
                finall_string = ""
                
                self.pos_of_items[cases[position_of_input][0]][cases[position_of_input][1]] = self.player
                
                for i in proccesing_str:
                    finall_string += i
                self.play_field[pos[0]][0] = finall_string
                self.draw()

            else:
                self.player_turn()
                return 
        else:
            self.player_turn()
            
    #add_score module which adds points to self.player_score         
    def add_score(self):
        if self.player == "x":
            self.player_score["first_player"]+=1
        else:
            self.player_score["second_player"]+=1
    
    #module which prints winner after winning round
    def winner_stat(self):
        player_name = self.names()
        print("Winner is: " + player_name)
        self.add_score()
        self.running = False
        
    def check_winner(self):
        for row in self.pos_of_items:
            if row[0] == row[1] == row[2] != 0:
                self.winner_stat()
                break
        
        i = 0
        for index in range(len(self.pos_of_items)):
            if self.pos_of_items[i][index] == self.pos_of_items[i+1][index] == self.pos_of_items[i+2][index] !=0 :
                self.winner_stat()
                break
                
        if self.pos_of_items[0][0] == self.pos_of_items[1][1] == self.pos_of_items[2][2] !=0:
            self.winner_stat()
            return
        
        if self.pos_of_items[0][2] == self.pos_of_items[1][1] == self.pos_of_items[2][0] !=0:
            self.winner_stat()
            return
            
        if self.player == "x":
            self.player = "o"
        else:
            self.player = "x"

    
    def change_mode(self):
        change_mode = input("Do you wish to change mode(Y/N)?")
        if change_mode == "Y":
            if self.game_mode == "bot":
                self.game_mode = 'player'
                self.second_player = input("What's your name second player? ")
            else:
                self.game_mode = 'bot'
                self.second_player = "bot"
        elif change_mode =="N":
            pass
        else:
            self.change_mode()
            
    #module which asks if you want to play again and sets variables like they were at a begining of game    
    def game_over(self):
        continue_question = input("Do you wish to play again(Y/N)?")
        
        if continue_question == "Y":
            self.change_mode()
            self.running = True
            self.play_field = [[" | | "],
                                ["-----"],
                                [" | | "],
                                ["-----"],
                                [" | | "],]
            self.pos_of_items = [[0,0,0],[0,0,0],[0,0,0]]
            self.game_loop()
        elif continue_question == "N":
            print(f"""Stats \n {self.first_player}: {self.player_score["first_player"]} points and {self.second_player}: {self.player_score["second_player"]} points""")
        else:
            self.cont()
        
    def game_loop(self):
        while self.running:
            self.check_winner()
            if self.running:
                self.player_turn()
                
        self.game_over()
                
