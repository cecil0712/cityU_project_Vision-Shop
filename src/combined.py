from route_planning import get_route
from database_connect import *
from text_detection import OCR
from speech import speak_item,SpeakText,play_audio

def get_direction(start,end):
    '''
    return the direction in spoken form
    '''
    if end[0]-start[0]==1: # row diff = +1
        play_audio('./assets/audio/foward.wav') # foward
    elif end[0]-start-[0]==-1: # row diff = -1
        play_audio('./assets/audio/backward.wav')   # backward
    elif end[1]-start[1]==1: # column diff = +1
        play_audio('./assets/audio/right.wav') # rightward
    elif end[1]-start[1]==1: # column diff = -1
        play_audio('./assets/audio/left.wav') # leftward

map=get_map()

#input the required item name
text=speak_item(get_item_list())
if check_discount(text):
    play_audio('assets/audio/discount.wav')
destination=get_item_coor(text)
play_audio('assets/audio/directing.wav')

#a. plan the route from entry
current_brand=OCR(img)
start=get_item_coor(current_brand)
route=get_route(start,destination)
current_coor=start

route_num=0 # be the pointer to the route_list
while current_coor!=route[-1]: # if user is not at the destination
    direction=get_direction(route[route_num],route[route_num+1]) # to tell the user what's the next step
    SpeakText(direction)
    current_brand=check_exist(OCR(img)) # if find the brand existed in the database, check user's location
    current_coor=get_region_coor(current_brand) # convert the brand title to coor
    if current_coor==route[route_num]: # if the user is on the correct location,ie. follow the route
        route_num+=1 # update it and find the next direction
    else:
        play_audio('assets/audio/redirecting.wav')
        route=get_route(current_coor,destination) # redirect the route
        route_num=0 # initialize the num
else:
    play_audio('assets/audio/arrive.wav')