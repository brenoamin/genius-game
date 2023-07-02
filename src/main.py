from tupy import *
from utils.buttons_mode import YELLOW_ON, GREEN_ON, RED_ON, BLUE_ON, YELLOW_OFF, GREEN_OFF, RED_OFF, BLUE_OFF, \
    BACKGROUND_SCENE, START, START_OFF

from utils.positive_reinforcement_phrases import positive_reinforcement_phrases
from utils.negative_reinforcement_phrases import negative_reinforcement_phrases

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
            BLUE_ON: BLUE_OFF,
            START: START_OFF,
            START_OFF: START
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


class StartButton(Button):
    def __init__(self, game, file=START, x=447, y=315, off_file=START):
        super().__init__(file, x, y, off_file)
        self.game = game

    def press(self):
        super().press()
        game.start_animation()



class ColoredButton(Button):
    def __init__(self, file, x, y, off_file):
        super().__init__(file, x, y, off_file)

    def press(self):
        super().press()
        game.check_sequence(self) 



class Game(Image):
    INITIAL_LEVEL = 1
    ANIMATION_DURATION = 60

    def __init__(self):
        self.file = BACKGROUND_SCENE
        self.x = 450
        self.y = 270
        self.sequence = []
        self.next_step = 0
        self.level = Game.INITIAL_LEVEL
        self.blink_index = 0
        self.blink_counter = 0
        self.blink_interval = 30
        self.sequence_delay_counter = 0
        self.start_counter = 100  # Quando instanciamos o jogo é necessário que o start_counter seja maior que o start_timer para que ele aguarde o acionamento do startbutton
        self.start_timer = 75  # Tempo de espera para gerar uma nova sequência por meio da função game.start()
        self.animation_counter = 0  # Contador para controlar a animação inicial
        self.is_animating = False

    def set_buttons(self, buttons):
        self.buttons = buttons

    def set_start_button(self, start_button):
        self.start_button = start_button

    def start(self):  # Redefine o nível inicial e zera o contador
        self.level = Game.INITIAL_LEVEL
        self.start_counter = 0  # Zera o contador toda vez que o botão é apertado, desse modo é possível resetar o jogo

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
    def start_animation(self):
        self.is_animating = True
        self.animation_counter = 0

        for button in self.buttons:
            button.start_blink()

    def check_sequence(self, button):
        expect = self.sequence[self.next_step]
        pressed_button = self.buttons.index(button)
        if pressed_button == expect:
            self.next_step += 1
            if self.next_step == len(self.sequence):
                reinforcement_phrase = random.choice(positive_reinforcement_phrases)
                print(reinforcement_phrase)
                self.sequence_delay_counter = 0
                self.level += 1
                self.sequence_delay_counter = 1
        else:
            reinforcement_phrases = random.choice(negative_reinforcement_phrases)
            print(reinforcement_phrases)
            self.next_step = 0
            self.level = Game.INITIAL_LEVEL

    def update(self):
        if self.is_animating:
            if self.animation_counter < Game.ANIMATION_DURATION:
                for button in self.buttons:
                    button.update()
                self.animation_counter += 1
            else:
                for button in self.buttons:
                    button.stop_blink()

                self.is_animating = False
                self.new_sequence()

        else:
            if self.blink_index < len(self.sequence):
                self.blink_buttons()

            if self.sequence_delay_counter > 0:
                self.sequence_delay_counter += 1
                if self.sequence_delay_counter >= SEQUENCE_DELAY_DURATION:
                    self.sequence_delay_counter = 0
                    self.new_sequence()

            self.start_counter += 1
            if self.start_counter == self.start_timer:
                self.start_counter = 0
                self.start_animation()  


if __name__ == '__main__':
    game = Game()

    start_button = StartButton(game)
    yellow_button = ColoredButton(YELLOW_OFF, 321, 396, YELLOW_OFF)
    red_button = ColoredButton(RED_OFF, 572, 145, RED_OFF)
    blue_button = ColoredButton(BLUE_OFF, 578, 395, BLUE_OFF)
    green_button = ColoredButton(GREEN_OFF, 320, 145, GREEN_OFF)
    game.set_buttons([yellow_button, red_button, blue_button, green_button])
    game.set_start_button(start_button)

    run(globals())
