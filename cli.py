

import speech_recognition as sr

import requests

import os 

import configparser
config = configparser.ConfigParser()
config.read('config.ini')

# speak structure for non-Debian OSs

import pyttsx3
engine = pyttsx3.init()
engine.say("I will speak this text")



# speak structure for Debian OSs
'''
import espeak
espeak.init()
speaker = espeak.Espeak()
speaker.say("Hello world")
speaker.rate = 300
speaker.say("Faster hello world")
'''

game_id=None

def create_game(size,handicap,komi):
    r= requests.get('http://127.0.0.1:5000/create_game/')
    game_id = 12

def is_blindfolded_player_black(game_id):
    r= requests.get('http://127.0.0.1:5000/is_blindfolded_player_black/')
    return True

def request_move_from_server(game_id):
    r= requests.get('http://127.0.0.1:5000/request_move_from_server/')
    return "D4" 

def is_game_over(game_id):
    r= requests.get('http://127.0.0.1:5000/is_game_over/')
    return False

def play_move(game_id, move):
    r= requests.get('http://127.0.0.1:5000/submit_move/') 

def is_move(game_id, move):
    r= requests.get('http://127.0.0.1:5000/is_move/')
    return True  

def is_playable_move(game_id, move):
    r= requests.get('http://127.0.0.1:5000/is_playable_move/')
    return True  

size=int(config['GOBAN']['size'])
handicap=int(config['HANDICAP']['number_of_stones'])
komi=float(config['RULES']['komi'])
game_id=create_game(size,handicap,komi)

r = sr.Recognizer()
mic = sr.Microphone()
sr.Microphone.list_microphone_names()

blindfolded_player_is_black=is_blindfolded_player_black(game_id)
label_dict={True:"black", False:"white"}
os.system("say 'Blindfolded player plays with the "+label_dict[blindfolded_player_is_black]+" stones !'") 
os.system("say 'Game started !'")

if not blindfolded_player_is_black:
    move=request_move_from_server(game_id)
    os.system("say 'White plays "+move+" !'")


while(is_game_over(game_id)==False):

    result=""

    while(is_move(game_id,move)==False):
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            result=r.recognize_google(audio)
        except sr.UnknownValueError:
            # speech was unintelligible
            result=""



    if is_playable_move(game_id,move):
        play_move(game_id,move)
        if result == "pass":
            os.system("say '"+label_dict[blindfolded_player_is_black]+" passes !'")
        elif result == "resign":
            os.system("say '"+label_dict[blindfolded_player_is_black]+" resigns !'") 
        else:
            os.system("say '"+label_dict[blindfolded_player_is_black]+" plays "+result+" !'") 
    else:
        os.system("say 'This move can't be played !'")

    if is_game_over(game_id):
        break
    else:
        move_from_AI=request_move_from_server(game_id)
        os.system("say '"+label_dict[blindfolded_player_is_black==False]+" plays "+move_from_AI+" !'")


    print(result)

os.system("say 'Thanks for the game !'")