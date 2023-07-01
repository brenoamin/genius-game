from tupy import *
from utils.buttons_mode import YELLOW_ON, GREEN_ON, RED_ON, BLUE_ON, YELLOW_OFF, GREEN_OFF, RED_OFF, BLUE_OFF, \
    BACKGROUND_SCENE, START
import random

PRESS_DURATION = 30
SEQUENCE_DELAY_DURATION = 120

class Button(Image):
    def __init__(self, file, x, y, off_file):
        self.file = file
        self.x = x
        self.y = y
        self.off_file = off_file
        self.is_blinking = False
        self.blink_interval = 20 
        self.blink_counter = 0
        self.is_button_on = False
        self.is_pressing = False
        self.press_counter = 0

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

    def start_blink(self):
        self.is_blinking = True
        self.blink_counter = 0
        self.is_button_on = True

    def stop_blink(self):
        self.is_blinking = False
        self.file = self.off_file 
        self.is_button_on = False

    def press(self):
        if not self.is_pressing:
            self.is_pressing = True
            self.press_counter = 0
            self.start_blink()
            game.check_sequence(self)

    def update(self):
        if self.is_blinking:
            self.blink_counter += 1
            if self.blink_counter >= self.blink_interval:
                self.toggle()
                self.blink_counter = 0
        
        if self.is_pressing:
            self.press_counter += 1
            if self.press_counter >= PRESS_DURATION:
                self.is_pressing = False
                self.stop_blink()

class Game(Image):
    INITIAL_LEVEL = 1
    def __init__(self):
        self.file = BACKGROUND_SCENE
        self.x = 450
        self.y = 270
        self.sequence = []
        self.next_step = 0
        self.level = Game.INITIAL_LEVEL
        self.blink_index = 0
        self.blink_counter = 0
        self.sequence_delay_counter = 0
        self.blink_interval = 30 

    def set_buttons(self, buttons):
        self.buttons = buttons

    def new_sequence(self):
        self.sequence = [random.randint(0, 3) for _ in range(self.level)]
        self.next_step = 0
        self.blink_index = 0
        self.blink_counter = 0

        return self.sequence

    def blink_buttons(self):
        if self.blink_index >= len(self.sequence):
            for button in self.buttons:
                button.stop_blink()
            return

        button = self.buttons[self.sequence[self.blink_index]]
        if self.blink_counter == 0:
            button.start_blink()
        elif self.blink_counter >= self.blink_interval:
            button.stop_blink()

        self.blink_counter += 1
        if self.blink_counter >= self.blink_interval * 2:
            self.blink_counter = 0
            self.blink_index += 1

    def check_sequence(self, button):
        expect = self.sequence[self.next_step]
        pressed_button = self.buttons.index(button)
        if pressed_button == expect:
            self.next_step += 1
            print("correto")
            if self.next_step == len(self.sequence):
                print("You won!")
                self.sequence_delay_counter = 0
                self.level += 1
                self.sequence_delay_counter = 1
        else:
            print("You lost!")
            self.next_step = 0
            self.level = Game.INITIAL_LEVEL

    def update(self):
        if self.blink_index < len(self.sequence):
            self.blink_buttons()

        if self.sequence_delay_counter > 0:
            self.sequence_delay_counter += 1
            if self.sequence_delay_counter >= SEQUENCE_DELAY_DURATION:
                self.sequence_delay_counter = 0
                self.new_sequence()

if __name__ == '__main__':
    game = Game()

    yellow_button = Button(YELLOW_OFF, 321, 396, YELLOW_OFF)
    red_button = Button(RED_OFF, 572, 145, RED_OFF)
    blue_button = Button(BLUE_OFF, 578, 395, BLUE_OFF)
    green_button = Button(GREEN_OFF, 320, 145, GREEN_OFF)
    game.set_buttons([yellow_button, red_button, blue_button, green_button])

    run(globals())
