from tupy import *
from time import sleep
from utils.buttons_mode import YELLOW_ON, YELLOW_OFF, GREEN_ON, GREEN_OFF, RED_ON, RED_OFF, BLUE_ON, BLUE_OFF, BLACK
from threading import Timer

class Button(Image):
    def __init__(self, file, x, y):
        self.file = file
        self.x = x
        self.y = y

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
        Timer(1, self.toggle).start()





if __name__ == '__main__':
    yellow_button = Button(YELLOW_OFF, 500, 500)
    red_button = Button(RED_OFF,200, 100)
    run(globals())