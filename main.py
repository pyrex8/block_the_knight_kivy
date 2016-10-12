__version__='1'

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.utils import platform
from kivy.config import Config


Config.set('graphics', 'width', '284')
Config.set('graphics', 'height', '160')

from atari import *
from nemesis import *
from level import *


blocky = []

blocky =  ['XXXX    '
          ,'XXXX    '
          ,'XXXX    '
          ,'XXXX    ']
       

pf_left =   []
pf_right =  []

for i in range(len(level)):
    w = str(level[i])
    firstpart = str(w[:20])
    secondpart = str(w[20:])
    pf_left.append( firstpart )
    pf_right.append( secondpart )


class LoopGame(Widget):
    blip = SoundLoader.load('blip.wav')
    crash = SoundLoader.load('crash.wav')

    pixel_x = 1.0
    pixel_y = 1.0

    left0 = False
    right0 = False
    up0 = False
    down0 = False
    fire0 = False

    direction0 = 0

    NUM_LEVELS = 30

    sound_type = 0
    freq_number = 0
    sound_number = 1

    anamation = 0.0

    nemesis_y = 42.0
    direction1 = -1.0
    fire = 0
    fire_x = 0
    fire_y = 0
    fire_v = 0

    retries = 0
    level_number = 1
    field_width = 12

    skip_level = 0
    game_done = 0

    t = 0
    pos_x = 4
    pos_y = (SCREEN_Y/2 + field_width) * 50
    vel_x = 0
    vel_y = 0
    height0 = 4
    direction0 = -1.0

    jumping = 0 


    color_p0 = 2 + (8 * 3)
    color_p1 = 1 + (8 * 5)
    color_pf = 3 + (8 * 8)
    color_bk1 = 0 + (8 * 1)
    color_bk2 = 7 + (8 * 1)

    def __init__(self, **kwargs):
        super(LoopGame, self).__init__(**kwargs)
        if platform != 'android':
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def update(self, dt):

        if dt > 0.100:
            dt = 0.100

        if self.right0 == False:

            dt = dt*400

            self.pixel_x = float(self.width)/SCREEN_X
            self.pixel_y = float(self.height)/SCREEN_Y

        

            self.canvas.clear()
            with self.canvas:
                reset_collision()
                background(self, 0, SCREEN_Y, self.color_bk1)
                background(self, SCREEN_Y/2 - self.field_width, 2* self.field_width, self.color_bk2)

                self.anamation += dt/100.0
                if self.anamation >= 2.0:
                    self.anamation = 0.0

                d = int(self.fire_x/50)

                if self.level_number < self.NUM_LEVELS and self.vel_x > 0: 
                    self.nemesis_y += self.direction1 * dt/100.0 
                    missile1(self, d, self.fire_y + 6, 1, 1, self.color_p1)

                if self.nemesis_y < (SCREEN_Y/2 - self.field_width) - 4:
                    self.nemesis_y = 42.0

                if self.nemesis_y > (SCREEN_Y/2 + self.field_width) + 4:
                    self.nemesis_y = 42.0

                self.pos_x +=  self.vel_x * dt/50.0
                self.pos_y += self.vel_y * dt/50.0


                if self.pos_y > (SCREEN_Y/2 + self.field_width) * 50:
                    self.vel_y = 0
                    self.pos_y = (SCREEN_Y/2 + self.field_width) * 50
                    self.jumping = 0
                    self.direction0 = -1.0

                if self.pos_y < (SCREEN_Y/2 - self.field_width + self.height0) * 50:
                    self.vel_y = 0
                    self.pos_y = (SCREEN_Y/2 - self.field_width + self.height0)*50
                    self.jumping = 0
                    self.direction0 = 1.0

                if self.pos_x > (SCREEN_X + 7)*50:
                    self.level_number += 1
                    if self.level_number > self.NUM_LEVELS:
                        self.level_number = self.NUM_LEVELS
                    self.pos_x = 0
                    self.pos_y = (SCREEN_Y/2 + self.field_width)*50
                    self.jumping = 0
                    self.direction0 = -1.0
                    self.color_p0 = (self.color_p0 + 8) & 0x7F
                    self.color_p1 = (self.color_p1 + 8) & 0x7F 
                    self.color_pf = (self.color_pf + 8) & 0x7F
                    self.color_bk1 = (self.color_bk1 + 8) & 0x7F
                    self.color_bk2 = (self.color_bk2 + 8) & 0x7F
                    self.fire = 0


                if self.level_number == self.NUM_LEVELS:
                    self.pos_x = (SCREEN_X- 14)*50
                    self.pos_y = (SCREEN_Y/2 + 2) * 50
                player0(self, int(self.pos_x/50), int(self.pos_y/50)-4, blocky, self.color_p0)

                a = int(self.anamation)
                b = self.level_number - 1
                c = int(self.nemesis_y)
                for i in range(6):
                    playfield(self, 40 + 4*i, 4, pf_left[i+6*b], self.color_pf, 1, 0)
                    playfield(self, 40 + 4*i, 4, pf_right[i+6*b], self.color_pf, 0, 1)

                if self.direction1 < 0:
                    missile0(self, 152, SCREEN_Y/2 - self.field_width - 1, 8, 1, self.color_p0) 
                else:
                    missile0(self, 152, SCREEN_Y/2 + self.field_width, 8, 1, self.color_p0)    

                if self.fire == 0:
                    self.fire = 1
                    self.fire_x = 152 * 50
                    self.fire_y = c
                    self.fire_v = -120
                else:
                    self.fire_x += self.fire_v*dt/50.0

                if self.fire_x < 0:
                    self.fire_x = 0
                    self.fire = 0

                player1(self, 152, c, nemesis[(b*24)+(a*12):(b*24)+(a*12)+12]
                    , self.color_p1)


                if self.retries > 999:
                    self.retries = 999

                number(self, 9, 2, self.retries, self.color_p0)
                number(self, 24, 2, self.level_number, self.color_p0)

                print_large(self, 28, 2, '-30', self.color_p0)

                # Start screen
                if self.vel_x == 0 and self.level_number == 1:
                    self.vel_x = 0
                    self.vel_y = 0
                    self.pos_x = 0 
                    self.pos_y = (SCREEN_Y/2 + self.field_width) * 50 
                    print_large(self, 2, 2+16, '   TAP', self.color_p0)
                    print_large(self, 2, 2+24, ' TO START', self.color_p0)


                # End SCREEN
                if self.level_number == self.NUM_LEVELS:
                    self.vel_x = 0
                    self.vel_y = 0
                    self.pos_x = 0
                    self.pos_y = (SCREEN_Y/2 + self.field_width) * 50    
                    print_large(self, 2, 2+16, '   YOU', self.color_p0)
                    print_large(self, 2, 2+24,  ' DID IT!', self.color_p0)


                if get_collision(P0, P1):
                    if self.crash:
                        self.crash.play()
                    self.retries += 1
                    self.vel_y = 0
                    self.pos_x = 0
                    self.pos_y = (SCREEN_Y/2 + self.field_width) * 50
                    self.jumping = 0
                    self.direction0 = -1.0
                    self.fire = 0

                if get_collision(P0, M1):
                    if self.crash:
                        self.crash.play()
                    self.retries += 1
                    self.vel_y = 0
                    self.pos_x = 0
                    self.pos_y = (SCREEN_Y/2 + self.field_width) * 50
                    self.jumping = 0
                    self.direction0 = -1.0
                    self.fire = 0

                if get_collision(M1, PF):
                    self.fire = 0

                if get_collision(P0, PF):
                    if self.crash:
                        self.crash.play()
                    self.retries += 1
                    self.vel_y = 0
                    self.pos_x = 0
                    self.pos_y = (SCREEN_Y/2 + self.field_width) * 50
                    self.jumping = 0
                    self.direction0 = -1.0
                    self.fire = 0

                if get_collision(P1, M0):
                    self.direction1 = -self.direction1

                if self.fire0 == True:
                    self.fire0 = False
                    if self.vel_x > 0:
                        if self.jumping == 0:
                            if self.blip:
                                self.blip.play()                        
                            self.jumping = 1
                            self.vel_y = 180 * self.direction0
                    else:
                        self.vel_x = 240

    def on_touch_down(self, touch):
        self.fire0 = True 
   

    def on_touch_up(self, touch):
        self.left0 = False
#        self.right0 = False
        self.up0 = False
        self.down0 = False
        self.fire0 = False
        self.skip_level = 0


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.left0 = False
        self.right0 = False
        self.up0 = False
        self.down0 = False
        self.fire0 = False
        self.skip_level = 0
        if keycode[1] == 'spacebar':
            self.fire0 = True 
        elif keycode[1] == 'up':
            self.up0 = True
            self.skip_level = 0 
        elif keycode[1] == 'down':
            self.down0 = True 
        elif keycode[1] == 'left':
            self.left0 = True 
        elif keycode[1] == 'right':
            self.right0 = True             
        return True
  


class LoopApp(App):
#    title = 'Basic Application'
    game = 1
    def build(self):
        self.game = LoopGame()
        Clock.schedule_interval(self.game.update, 1.0 / 20.0)
        return self.game

    def on_pause(self):
        # Here you can save data if needed
        self.game.right0 = True
        return True
        
    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        self.game.right0 = False


if __name__ == '__main__':
    LoopApp().run()
