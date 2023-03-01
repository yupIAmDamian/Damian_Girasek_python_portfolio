from vars import *
from field import Game

mode = input("Do you prefer playing agains bot or player? Write bot or player: ")
first_player_name = input("What's your name ")
if mode == "player":
    second_player_name = input("What's your name second player? ")
else:
    second_player_name = "bot"
    
game = Game(playing_field,mode,first_player_name,second_player_name)
game.game_loop()

