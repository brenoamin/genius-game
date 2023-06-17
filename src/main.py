from tupy import *
from utils.buttons_mode import YELLOW_ON, GREEN_ON, RED_ON, BLUE_ON, YELLOW_OFF, GREEN_OFF, RED_OFF, BLUE_OFF, BACKGROUND_SCENE

class Field(Image):
    def __init__(self):
        self.file = BACKGROUND_SCENE
        self.x = 800
        self.y = 600


class Button(Image):
    def __init__(self, file, x, y):
        self.file = file
        self.x = x
        self.y = y
        self.toggle_count = 0
        self.toggle_limit = 30

    def toggle(self):
        mapping = {
            YELLOW_OFF: YELLOW_ON,
            GREEN_OFF: GREEN_ON,
            RED_OFF: RED_ON,
            BLUE_OFF: BLUE_ON,
            YELLOW_ON: YELLOW_OFF,
            GREEN_ON: GREEN_OFF,
            RED_ON: RED_OFF,
            BLUE_ON: BLUE_OFF
        }

        if self.file in mapping:
            self.file = mapping[self.file]

    def press(self):
        self.toggle()
        self.toggle_count = self.toggle_limit 

    def decrement_toggle_count(self):
        if self.toggle_count > 0:
            self.toggle_count -= 1
            if self.toggle_count == 0:
                self.toggle()
                
    def update(self):
        self.decrement_toggle_count()
    

if __name__ == '__main__':
    field = Field()
    yellow_button = Button(YELLOW_ON, 490, 910)
    red_button = Button(RED_ON, 1110, 290)
    blue_button = Button(BLUE_ON, 1110, 910)
    green_button = Button(GREEN_ON, 480, 290)
    run(globals())