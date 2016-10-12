from kivy.graphics import Color, Rectangle, Ellipse
#import pyaudio
import array
import math
import time
import random



SCREEN_X = 160
SCREEN_Y = 104

PF_PIXEL = 4

NUMBER_OF_OBJECTS = 6
# bit xs for collison detection
# bl, pf, m1, p1, m0, p0
BL = 0
P0 = 1
M0 = 2
P1 = 3
M1 = 4
PF = 5


collision_detection = [0] * NUMBER_OF_OBJECTS
collision_array = [0] * (SCREEN_X * SCREEN_Y) 




colors_rgba = [ 
[ 0.0 , 0.0 , 0.0 , 1],
[ 0.25 , 0.25 , 0.25 , 1],
[ 0.421875 , 0.421875 , 0.421875 , 1],
[ 0.5625 , 0.5625 , 0.5625 , 1],
[ 0.6875 , 0.6875 , 0.6875 , 1],
[ 0.78125 , 0.78125 , 0.78125 , 1],
[ 0.859375 , 0.859375 , 0.859375 , 1],
[ 0.921875 , 0.921875 , 0.921875 , 1],
[ 0.265625 , 0.265625 , 0.0 , 1],
[ 0.390625 , 0.390625 , 0.0625 , 1],
[ 0.515625 , 0.515625 , 0.140625 , 1],
[ 0.625 , 0.625 , 0.203125 , 1],
[ 0.71875 , 0.71875 , 0.25 , 1],
[ 0.8125 , 0.8125 , 0.3125 , 1],
[ 0.90625 , 0.90625 , 0.359375 , 1],
[ 0.984375 , 0.984375 , 0.40625 , 1],
[ 0.4375 , 0.15625 , 0.0 , 1],
[ 0.515625 , 0.265625 , 0.078125 , 1],
[ 0.59375 , 0.359375 , 0.15625 , 1],
[ 0.671875 , 0.46875 , 0.234375 , 1],
[ 0.734375 , 0.546875 , 0.296875 , 1],
[ 0.796875 , 0.625 , 0.359375 , 1],
[ 0.859375 , 0.703125 , 0.40625 , 1],
[ 0.921875 , 0.78125 , 0.46875 , 1],
[ 0.515625 , 0.09375 , 0.0 , 1],
[ 0.59375 , 0.203125 , 0.09375 , 1],
[ 0.671875 , 0.3125 , 0.1875 , 1],
[ 0.75 , 0.40625 , 0.28125 , 1],
[ 0.8125 , 0.5 , 0.359375 , 1],
[ 0.875 , 0.578125 , 0.4375 , 1],
[ 0.921875 , 0.65625 , 0.5 , 1],
[ 0.984375 , 0.734375 , 0.578125 , 1],
[ 0.53125 , 0.0 , 0.0 , 1],
[ 0.609375 , 0.125 , 0.125 , 1],
[ 0.6875 , 0.234375 , 0.234375 , 1],
[ 0.75 , 0.34375 , 0.34375 , 1],
[ 0.8125 , 0.4375 , 0.4375 , 1],
[ 0.875 , 0.53125 , 0.53125 , 1],
[ 0.921875 , 0.625 , 0.625 , 1],
[ 0.984375 , 0.703125 , 0.703125 , 1],
[ 0.46875 , 0.0 , 0.359375 , 1],
[ 0.546875 , 0.125 , 0.453125 , 1],
[ 0.625 , 0.234375 , 0.53125 , 1],
[ 0.6875 , 0.34375 , 0.609375 , 1],
[ 0.75 , 0.4375 , 0.6875 , 1],
[ 0.8125 , 0.515625 , 0.75 , 1],
[ 0.859375 , 0.609375 , 0.8125 , 1],
[ 0.921875 , 0.6875 , 0.875 , 1],
[ 0.28125 , 0.0 , 0.46875 , 1],
[ 0.375 , 0.125 , 0.5625 , 1],
[ 0.46875 , 0.234375 , 0.640625 , 1],
[ 0.546875 , 0.34375 , 0.71875 , 1],
[ 0.625 , 0.4375 , 0.796875 , 1],
[ 0.703125 , 0.515625 , 0.859375 , 1],
[ 0.765625 , 0.609375 , 0.921875 , 1],
[ 0.828125 , 0.6875 , 0.984375 , 1],
[ 0.078125 , 0.0 , 0.515625 , 1],
[ 0.1875 , 0.125 , 0.59375 , 1],
[ 0.296875 , 0.234375 , 0.671875 , 1],
[ 0.40625 , 0.34375 , 0.75 , 1],
[ 0.484375 , 0.4375 , 0.8125 , 1],
[ 0.578125 , 0.53125 , 0.875 , 1],
[ 0.65625 , 0.625 , 0.921875 , 1],
[ 0.734375 , 0.703125 , 0.984375 , 1],
[ 0.0 , 0.0 , 0.53125 , 1],
[ 0.109375 , 0.125 , 0.609375 , 1],
[ 0.21875 , 0.25 , 0.6875 , 1],
[ 0.3125 , 0.359375 , 0.75 , 1],
[ 0.40625 , 0.453125 , 0.8125 , 1],
[ 0.484375 , 0.546875 , 0.875 , 1],
[ 0.5625 , 0.640625 , 0.921875 , 1],
[ 0.640625 , 0.71875 , 0.984375 , 1],
[ 0.0 , 0.09375 , 0.484375 , 1],
[ 0.109375 , 0.21875 , 0.5625 , 1],
[ 0.21875 , 0.328125 , 0.65625 , 1],
[ 0.3125 , 0.4375 , 0.734375 , 1],
[ 0.40625 , 0.53125 , 0.796875 , 1],
[ 0.484375 , 0.609375 , 0.859375 , 1],
[ 0.5625 , 0.703125 , 0.921875 , 1],
[ 0.640625 , 0.78125 , 0.984375 , 1],
[ 0.0 , 0.171875 , 0.359375 , 1],
[ 0.109375 , 0.296875 , 0.46875 , 1],
[ 0.21875 , 0.40625 , 0.5625 , 1],
[ 0.3125 , 0.515625 , 0.671875 , 1],
[ 0.40625 , 0.609375 , 0.75 , 1],
[ 0.484375 , 0.703125 , 0.828125 , 1],
[ 0.5625 , 0.796875 , 0.90625 , 1],
[ 0.640625 , 0.875 , 0.984375 , 1],
[ 0.0 , 0.234375 , 0.171875 , 1],
[ 0.109375 , 0.359375 , 0.28125 , 1],
[ 0.21875 , 0.484375 , 0.390625 , 1],
[ 0.3125 , 0.609375 , 0.5 , 1],
[ 0.40625 , 0.703125 , 0.578125 , 1],
[ 0.484375 , 0.8125 , 0.671875 , 1],
[ 0.5625 , 0.890625 , 0.75 , 1],
[ 0.640625 , 0.984375 , 0.828125 , 1],
[ 0.0 , 0.234375 , 0.0 , 1],
[ 0.125 , 0.359375 , 0.125 , 1],
[ 0.25 , 0.484375 , 0.25 , 1],
[ 0.359375 , 0.609375 , 0.359375 , 1],
[ 0.453125 , 0.703125 , 0.453125 , 1],
[ 0.546875 , 0.8125 , 0.546875 , 1],
[ 0.640625 , 0.890625 , 0.640625 , 1],
[ 0.71875 , 0.984375 , 0.71875 , 1],
[ 0.078125 , 0.21875 , 0.0 , 1],
[ 0.203125 , 0.359375 , 0.109375 , 1],
[ 0.3125 , 0.484375 , 0.21875 , 1],
[ 0.421875 , 0.59375 , 0.3125 , 1],
[ 0.515625 , 0.703125 , 0.40625 , 1],
[ 0.609375 , 0.796875 , 0.484375 , 1],
[ 0.703125 , 0.890625 , 0.5625 , 1],
[ 0.78125 , 0.984375 , 0.640625 , 1],
[ 0.171875 , 0.1875 , 0.0 , 1],
[ 0.296875 , 0.3125 , 0.109375 , 1],
[ 0.40625 , 0.4375 , 0.203125 , 1],
[ 0.515625 , 0.546875 , 0.296875 , 1],
[ 0.609375 , 0.65625 , 0.390625 , 1],
[ 0.703125 , 0.75 , 0.46875 , 1],
[ 0.796875 , 0.828125 , 0.53125 , 1],
[ 0.875 , 0.921875 , 0.609375 , 1],
[ 0.265625 , 0.15625 , 0.0 , 1],
[ 0.390625 , 0.28125 , 0.09375 , 1],
[ 0.515625 , 0.40625 , 0.1875 , 1],
[ 0.625 , 0.515625 , 0.265625 , 1],
[ 0.71875 , 0.609375 , 0.34375 , 1],
[ 0.8125 , 0.703125 , 0.421875 , 1],
[ 0.90625 , 0.796875 , 0.484375 , 1],
[ 0.984375 , 0.875 , 0.546875 , 1]
]


#!/usr/bin/env python
''' 3x5 font http://robey.lag.net/2010/01/23/tiny-monospace-font.html'''



# starts at ASCII 32 - space
font_3x5 =  ['   '
            ,'   '
            ,'   '
            ,'   '
            ,'   '

            ,' X '
            ,' X '
            ,' X '
            ,'   '
            ,' X '

            ,'X X'
            ,'X X'
            ,'   '
            ,'   '
            ,'   '

            ,'X X'
            ,'XXX'
            ,'X X'
            ,'XXX'
            ,'X X'

            ,' XX'
            ,'XX '
            ,' XX'
            ,'XX '
            ,' X '

            ,'X  '
            ,'  X'
            ,' X '
            ,'X  '
            ,'  X'

            ,'XX '
            ,'XX '
            ,'XXX'
            ,'X X'
            ,' XX'

            ,' X '
            ,'   '
            ,'   '
            ,'   '
            ,'   '

            ,'  X'
            ,' X '
            ,' X '
            ,' X '
            ,'  X'

            ,'X  '
            ,' X '
            ,' X '
            ,' X '
            ,'X  '

            ,'X X'
            ,' X '
            ,'X X'
            ,'   '
            ,'   '

            ,'   '
            ,' X '
            ,'XXX'
            ,' X '
            ,'   '

            ,'   '
            ,'   '
            ,'   '
            ,' X '
            ,'X  '

            ,'   '
            ,'   '
            ,'XXX'
            ,'   '
            ,'   '

            ,'   '
            ,'   '
            ,'   '
            ,'   '
            ,' X '

            ,'  X'
            ,'  X'
            ,' X '
            ,'X  '
            ,'X  ']



digits =    ['XXX'
            ,'X X'
            ,'X X'
            ,'X X'
            ,'XXX'

            ,'  X'
            ,'  X'
            ,'  X'
            ,'  X'
            ,'  X'

            ,'XXX'
            ,'  X'
            ,'XXX'
            ,'X  '
            ,'XXX'

            ,'XXX'
            ,'  X'
            ,'XXX'
            ,'  X'
            ,'XXX'

            ,'X X'
            ,'X X'
            ,'XXX'
            ,'  X'
            ,'  X'

            ,'XXX'
            ,'X  '
            ,'XXX'
            ,'  X'
            ,'XXX'

            ,'XXX'
            ,'X  '
            ,'XXX'
            ,'X X'
            ,'XXX'

            ,'XXX'
            ,'  X'
            ,'  X'
            ,'  X'
            ,'  X'

            ,'XXX'
            ,'X X'
            ,'XXX'
            ,'X X'
            ,'XXX'

            ,'XXX'
            ,'X X'
            ,'XXX'
            ,'  X'
            ,'XXX'

            ,'   '
            ,' X '
            ,'   '
            ,' X '
            ,'   '

            ,'   '
            ,' X '
            ,'   '
            ,' X '
            ,'X  '

            ,'  X'
            ,' X '
            ,'X  '
            ,' X '
            ,'  X'            

            ,'   '
            ,'XXX'
            ,'   '
            ,'XXX'
            ,'   '

            ,'X  '
            ,' X '
            ,'  X'
            ,' X '
            ,'X  '

            ,'XXX'
            ,'  X'
            ,' X '
            ,'   '
            ,' X '

            ,' X '
            ,'X X'
            ,'XXX'
            ,'X  '
            ,' XX']




upper_c =   [' X '
            ,'X X'
            ,'XXX'
            ,'X X'
            ,'X X'

            ,'XX '
            ,'X X'
            ,'XX '
            ,'X X'
            ,'XX '

            ,' XX'
            ,'X  '
            ,'X  '
            ,'X  '
            ,' XX'

            ,'XX '
            ,'X X'
            ,'X X'
            ,'X X'
            ,'XX '

            ,'XXX'
            ,'X  '
            ,'XXX'
            ,'X  '
            ,'XXX'

            ,'XXX'
            ,'X  '
            ,'XXX'
            ,'X  '
            ,'X  '

            ,' XX'
            ,'X  '
            ,'XXX'
            ,'X X'
            ,' XX'

            ,'X X'
            ,'X X'
            ,'XXX'
            ,'X X'
            ,'X X'            

            ,'XXX'
            ,' X '
            ,' X '
            ,' X '
            ,'XXX'

            ,'  X'
            ,'  X'
            ,'  X'
            ,'X X'
            ,' X '

            ,'X X'
            ,'X X'
            ,'XX '
            ,'X X'
            ,'X X'

            ,'X  '
            ,'X  '
            ,'X  '
            ,'X  '
            ,'XXX'

            ,'X X'
            ,'XXX'
            ,'XXX'
            ,'X X'
            ,'X X'

            ,'X X'
            ,'XXX'
            ,'XXX'
            ,'XXX'
            ,'X X'

            ,'XXX'
            ,'X X'
            ,'X X'
            ,'X X'
            ,'XXX'

            ,'XX '
            ,'X X'
            ,'XX '
            ,'X  '
            ,'X  '

            ,' X '
            ,'X X'
            ,'X X'
            ,'X X'
            ,' XX'

            ,'XX '
            ,'X X'
            ,'XX '
            ,'XX '
            ,'X X'


            ,' XX'
            ,'X  '
            ,' X '
            ,'  X'
            ,'XX '

            ,'XXX'
            ,' X '
            ,' X '
            ,' X '
            ,' X '

            ,'X X'
            ,'X X'
            ,'X X'
            ,'X X'
            ,' XX'

            ,'X X'
            ,'X X'
            ,'X X'
            ,' X '
            ,' X '

            ,'X X'
            ,'X X'
            ,'XXX'
            ,'XXX'
            ,'X X'

            ,'X X'
            ,'X X'
            ,' X '
            ,'X X'
            ,'X X'

            ,'X X'
            ,'X X'
            ,' X '
            ,' X '
            ,' X '

            ,'XXX'
            ,'  X'
            ,' X '
            ,'X  '
            ,'XXX'

            ,'XXX'
            ,'X  '
            ,'X  '
            ,'X  '
            ,'XXX'

            ,'   '
            ,'X  '
            ,' X '
            ,'  X'
            ,'   '

            ,'XXX'
            ,'  X'
            ,'  X'
            ,'  X'
            ,'XXX' 

            ,' X '
            ,'X X'
            ,'   '
            ,'   '
            ,'   ' 

            ,'   '
            ,'   '
            ,'   '
            ,'   '
            ,'XXX' 

            ,'X  '
            ,' X '
            ,'   '
            ,'   '
            ,'   ' 
            ]







font_3x5 += digits + upper_c





def reset_collision():
    """Clear collisoin detection."""
    global collision_detection
    global collision_array

    collision_detection = [0] * NUMBER_OF_OBJECTS
    collision_array = [0] * (SCREEN_X * SCREEN_Y) 


def update_collision(new_object, x, y):    
    """Update array and collision registers."""
    global collision_detection
    global collision_array

    if (x >= 0 and x < SCREEN_X and y >= 0 and y < SCREEN_Y):
        collision_array[x + (y * SCREEN_X)] |= (1<<new_object)
        collision_detection[new_object] |= collision_array[x + (y * SCREEN_X)]


def test_for_object(test_object, x, y):    
    """Test to see what objects are in location."""
    global collision_array
    test_value = 0
    if (x >= 0 and x < SCREEN_X and y >= 0 and y < SCREEN_Y):
        if collision_array[x + (y * SCREEN_X)] & 1<<test_object:
            test_value = 1
    return test_value

def get_collision(first_object, second_object):
    """Performs a test between two objects (P0, M0, P1, M0, ,PF, BL)
     0 = no collision, 1 = collision."""   
    global collision_detection   
    test_value = 0

    if  (collision_detection[first_object] & 1<<second_object) > 0:
        test_value = 1

    if  (collision_detection[second_object] & 1<<first_object) > 0:
        test_value = 1

    return test_value


def background(self, y, height, color):
    """Background coloring, either full screen or sections."""
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])    
    Rectangle(pos=(0, ys -((y+height)*e)), size=(self.width, height*e))


def playfield_collision(x, y):
    """Prints a 3x5 digit using Playfield pixels"""
    update_collision(PF, x, y)
    update_collision(PF, x + 1, y)
    update_collision(PF, x + 2, y)
    update_collision(PF, x + 3, y)    


def place_character(self, x, y, character, color):
    """Prints a 3x5 font using Playfield pixels, numbers upper case and some 
    special characters"""
    if character < 32 or character > 96:
         character = 63
    character -= 32
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])
    for j in range(5):
        k = font_3x5[(character * 5) + j]
        for i in range(3):
            if k[i] == 'X':
                Rectangle(pos=((x+i)*d*PF_PIXEL, ys -(y+j+1)*e),
                 size=(d*PF_PIXEL, e))
                playfield_collision((x+i)*4, y + j)

def print_large(self, x, y, pstring, color):
    """Prints a numeric value that is right justified using 3x5 digits in 
    Playfield pixels."""
    for i in range(len(pstring)):
        j = ord(pstring[i])
        place_character(self, x + (i*4), y, j, color)



def place_digit(self, x, y, digit, color):
    """Prints a 3x5 digit using Playfield pixels"""
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])
    for j in range(5):
        k = digits[(digit * 5) + j]
        for i in range(3):
            if k[i] == 'X':
                Rectangle(pos=((x+i)*d*PF_PIXEL, ys -(y+j+1)*e),
                 size=(d*PF_PIXEL, e))
                playfield_collision((x+i)*4, y + j)


def number(self, x, y, value, color):
    """Prints a numeric value that is right justified using 3x5 digits in 
    Playfield pixels."""
    if value < 0:
        value -= value
    value_string = str(value)
    for i in range(len(value_string)):
        j = int(value_string[len(value_string) - 1 - i])
        place_digit(self, x - (i*4), y, j, color)


def playfield(self, y, height, data, color, left, right):
    """Playfield drawing and collision detection."""
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])
    if left == 2:
        for i in range(20):
            if data[i] == 'X':  
                Rectangle(pos=((SCREEN_X/2-4)*d-i*d*PF_PIXEL, ys - (y+height)*e),
                    size=(d*PF_PIXEL, e*height))
                for j in range(height):        
                    playfield_collision(SCREEN_X/2 - (i*4) - 4, y)

    if left == 1: 
        for i in range(20):
            if data[i] == 'X':
                Rectangle(pos=(i*d*PF_PIXEL, ys - (y+height)*e),
                    size=(d*PF_PIXEL, e*height))
                for j in range(height):       
                    playfield_collision(i*4, y + j)

    if right == 2:
        for i in range(20):
            if data[i] == 'X':  
                Rectangle(pos=((SCREEN_X-4)*d-i*d*PF_PIXEL, ys - (y+height)*e),
                    size=(d*PF_PIXEL, e*height))
                for j in range(height):   
                    playfield_collision(SCREEN_X - (i*4) - 4, y + j)

    if right == 1:
        for i in range(20):
            if data[i] == 'X':  
                Rectangle(pos=(SCREEN_X*d/2+i*d*PF_PIXEL, ys - (y+height)*e),
                    size=(d*PF_PIXEL, e*height))
                for j in range(height):  
                    playfield_collision(SCREEN_X/2 + (i*4), y + j)



def ball(self, x, y, width, height, color):
    """Ball drawing and collision detection."""
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])
    Rectangle(pos=((x)*d, ys -(y+height)*e), size=(d*width, e*height))
    for i in range(height): 
        for j in range(width):
            update_collision(BL, x + j, y + i)


def missile0(self, x, y, width, height, color):
    """Missile0 drawing and collision detection."""
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])
    Rectangle(pos=((x)*d, ys -(y+height)*e), size=(d*width, e*height))
    for i in range(height): 
        for j in range(width):
            update_collision(M0, x + j, y + i)


def missile1(self, x, y, width, height, color):
    """Missile1 drawing and collision detection."""
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])
    Rectangle(pos=((x)*d, ys -(y+height)*e), size=(d*width, e*height))
    for i in range(height): 
        for j in range(width):
            update_collision(M1, x + j, y + i)



def player0(self, x, y, data, color):
    """Player0 drawing and collision detection."""
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])
    for j in range(len(data)):
        k = data[j]
        for i in range(8):
            if k[i] == 'X':
                Rectangle(pos=((x+i)*d, ys -(y+j+1)*e), size=(d, e))
                update_collision(P0, x + i, y + j)


def player1(self, x, y, data, color):
    """Player1 drawing and collision detection."""
    d = self.pixel_x
    e = self.pixel_y
    ys = self.height
    Color(*colors_rgba[color])
    for j in range(len(data)):
        k = data[j]
        for i in range(8):
            if k[i] == 'X':
                Rectangle(pos=((x+i)*d, ys -(y+j+1)*e), size=(d, e))
                update_collision(P1, x + i, y + j)