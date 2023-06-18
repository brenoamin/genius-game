from tupy import *
from utils.buttons_mode import YELLOW_ON, GREEN_ON, RED_ON, BLUE_ON, YELLOW_OFF, GREEN_OFF, RED_OFF, BLUE_OFF, \
    BACKGROUND_SCENE, START
from time import sleep
from threading import Timer
import random

'''class Field(Image):
    def __init__(self):
        self.file = BACKGROUND_SCENE
        self.x = 450
        self.y = 270
'''

class Button(Image):
    def __init__(self, file, x, y):
        self.file = file
        self.x = x
        self.y = y
        self.toggle_count = 0
        self.toggle_limit = 30
       # self.pressed_button = False

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
        #self.pressed_button = True

    def decrement_toggle_count(self):
        if self.toggle_count > 0:
            self.toggle_count -= 1
            if self.toggle_count == 0:
                self.toggle()

    def update(self):
        self.decrement_toggle_count()

class Game(Image):
    def __init__(self):
        self.file = BACKGROUND_SCENE
        self.x = 450
        self.y = 270
        self.sequence = []
        self.next_step = 0
        self.level = 5
        self.ok = True
        # Quando instanciamos os botões dentro da classe game eles não recebem os nomes das variáveis, logo ficam numerados no tupy
        '''self.buttons = [
            Button(YELLOW_OFF, 321, 396),
            Button(RED_OFF, 572, 145),
            Button(BLUE_OFF, 578, 395),
            Button(GREEN_OFF, 320, 145),
            Button(START, 447, 314)
        ]'''
        self.toggle_count = 0
        self.toggle_limit = 60

    def set_buttons(self, buttons):
        self.buttons = buttons

    def new_sequence(self):
        """gera uma sequência com "n" passos.
        0 -> Amarelo
        1 -> Vermelho
        2 -> Azul
        3 -> Verde
        """
        self.sequence = [random.randint(0, 3) for _ in range(self.level)]
        self.next_step = 0
        self.test_sequence()

        for valor in self.sequence:
            print(f"valor - {valor}")
            Timer(10, self.buttons[valor].press()).start()
            print(f'Botão {self.buttons[valor]} ligado')

        return self.sequence

    #def button_click(self, valor):
     #   self.buttons[valor].press()

    def test_sequence(self):
        print(self.sequence)


if __name__ == '__main__':

    game = Game()
    yellow_button = Button(YELLOW_OFF, 321, 396)
    red_button = Button(RED_OFF, 572, 145)
    blue_button = Button(BLUE_OFF, 578, 395)
    green_button = Button(GREEN_OFF, 320, 145)
    game.set_buttons([yellow_button, red_button, blue_button, green_button])

    run(globals())