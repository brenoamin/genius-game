from tupy import *
from utils.buttons_mode import YELLOW_ON, GREEN_ON, RED_ON, BLUE_ON, YELLOW_OFF, GREEN_OFF, RED_OFF, BLUE_OFF, \
    BACKGROUND_SCENE, START, START_OFF
from enum import Enum

from utils.positive_reinforcement_phrases import positive_reinforcement_phrases
from utils.negative_reinforcement_phrases import negative_reinforcement_phrases

import random

from typing import Any, List

PRESS_DURATION = 30
SEQUENCE_DELAY_DURATION = 120


class Player:
    """
    Representa um jogador no jogo.

    Atributos:
        _score (int): O score atual do jogador, armazenado de forma privada.
    
    Método:
        increase_score(): Incrementa o score do jogador em 1 unidade.

    Uso:
        player = Player()
        player.increase_score()
        print(player.score)  # Imprime o score atual do jogador
    """
    def __init__(self) -> None:
        self._score = 0

    def increase_score(self) -> None:
        self._score += 1

    @property
    def score(self)-> int:
        return self._score


class Button(Image):
    """
    Classe que representa os botões do jogo.

    Esta classe herda da classe Image e adiciona métodos para controlar o estado dos botões.

    Atributos:
        file (Image): imagem do botão.
        x (int): posição horizontal do botão na tela.
        y (int): posição vertical do botão na tela.
        off_file (Image): imagem do botão desligado.
        is_blinking (bool): status do piscar da luz do botão.
        blink_interval (int): intervalo em que a luz do botão pisca.
        blink_counter (int): contador usado para controlar o piscar da luz do botão.
        is_button_on (bool): status do botão ligado ou desligado.
        is_pressing (bool): status de pressionamento do botão.
        press_counter (int): contador usado para controlar o tempo de pressionamento do botão.

    Métodos:
        __init__(self, file: Image, x: int, y: int, off_file: Image): 
            Inicializa a classe Button com as imagens, posição e status fornecidos.
        toggle(self) -> None:
            Alterna o estado do botão entre ligado e desligado.
        start_blink(self) -> None:
            Inicia o piscar da luz do botão.
        stop_blink(self) -> None:
            Para o piscar da luz do botão.
        press(self) -> None:
            Processa o pressionamento do botão e inicia o piscar da luz do botão.
        update(self) -> None:
            Atualiza o estado da luz do botão de acordo com o status de piscar e pressionamento.

    """

    def __init__(self, file: Image, x: int, y: int, off_file: Image):
        """
        Inicializa a classe Button.

        Returns:
            None
        """
        

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

    def toggle(self) -> None:
        """
        Alterna o estado do botão.

        Esta função alterna o estado do botão entre ligado e desligado.

        Retorna:
            None
        """
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

    def start_blink(self) -> None:
        """
        Inicia o piscar da luz.

        Esta função define as variáveis de estado para iniciar o piscar das luzes dos botoes.

        Retorna:
            None
        """
        self.is_blinking = True
        self.blink_counter = 0
        self.is_button_on = True

    def stop_blink(self) -> None:
        """
        Para o piscar da luz.

        Esta função define as variáveis de estado para parar o piscar das luzes dos botoes.

        Retorna:
            None
        """
        self.is_blinking = False
        self.file = self.off_file
        self.is_button_on = False

    def press(self) -> None:
        """
        Processa o pressionamento do botão.

        Esta função é chamada quando o botão é pressionado e inicia o piscar da luz do botão.

        Retorna:
            None
        """
        if not self.is_pressing:
            self.is_pressing = True
            self.press_counter = 0
            self.start_blink()

    def update(self) -> None:
        """
        Atualiza o estado da luz.

        Esta função é chamada periodicamente para atualizar o estado da luz.
        Se a luz estiver piscando, ela alterna o estado da luz de acordo com o intervalo definido.
        Se o botão estiver pressionado, ela conta o tempo de pressionamento e para o piscar da luz depois de um tempo definido.

        Retorna:
            None
        """
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
    """
    Classe que representa o botão de início do jogo.

    Esta classe herda da classe Button e adiciona um status de início para controlar o estado do botão.

    Atributos:
        game (Any): instância do jogo que utiliza o botão.
        start_status (bool): status do botão de início.
        
    Métodos:
        __init__(self, game: Any, file=START, x: int=447, y: int=315, off_file=START): 
            Inicializa a classe StartButton com o arquivo, posição e instância de jogo fornecidos.
            
        press(self) -> None:
            Processa o pressionamento do botão e inicia a animação de início do jogo.
            
        toggle_status(self) -> None:
            Alterna o status do botão de início entre ligado e desligado.

    """
    def __init__(self, game: Any, file=START, x: int=447, y: int=315, off_file=START):
        """
        Inicializa a classe StartButton.

        Argumentos:
            game (Any): instância do jogo que utiliza o botão.
            file (str): caminho para o arquivo de imagem do botão.
            x (int): posição horizontal do botão na tela.
            y (int): posição vertical do botão na tela.
            off_file (str): caminho para o arquivo de imagem do botão desligado.

        Retorna:
            None
        """
        super().__init__(file, x, y, off_file)
        self.game = game
        self.start_status = False

    def press(self) -> None:
        """
        Processa o pressionamento do botão.

        Esta função é chamada quando o botão é pressionado e inicia a animação de início do jogo.

        Retorna:
            None
        """
        super().press()
        self.toggle_status()
        game.start_animation()

    def toggle_status(self) -> None:
        """
        Altera o status do botão de início.

        Esta função alterna o status do botão de início entre ligado e desligado.

        Retorna:
            None
        """
        mapping = {
            True: False,
            False: True
        }

        if self.start_status in mapping:
            self.start_status = mapping[self.start_status]


class ColoredButton(Button):
    """
    Classe que representa os botões coloridos do jogo.

    Esta classe herda da classe Button e adiciona um método para processar o pressionamento do botão.

    Métodos:
        __init__(self, file: Button, x: int, y: int, off_file: Button): 
            Inicializa a classe ColoredButton com as imagens, posição e status fornecidos.
            
        press(self) -> None:
            Processa o pressionamento do botão e verifica a sequência de cores.

    """
    def __init__(self, file: Button, x: int, y: int, off_file: Button):
        """
        Inicializa a classe ColoredButton.

        Argumentos:
            file (Button): imagem do botão colorido.
            x (int): posição horizontal do botão na tela.
            y (int): posição vertical do botão na tela.
            off_file (Button): imagem do botão desligado.

        Retorna:
            None
        """
        super().__init__(file, x, y, off_file)

    def press(self) -> None:
        """
        Processa o pressionamento do botão.

        Esta função é chamada quando o botão é pressionado e verifica a sequência de cores do jogo.

        Retorna:
            None
        """
        if start_button.start_status:
            super().press()
            game.check_sequence(self)


class Game(Image):
    """
    Classe que representa o jogo Ginius.

    Esta classe herda da classe Image e adiciona métodos para gerenciar o jogo e processar a sequência de cores.

    Atributos:
        INITIAL_LEVEL (int): nível inicial do jogo.
        ANIMATION_DURATION (int): duração da animação de início do jogo.
        file (Image): imagem de fundo do jogo.
        x (int): posição horizontal da imagem.
        y (int): posição vertical da imagem.
        sequence (List[int]): sequência de cores gerada pelo jogo.
        next_step (int): próximo passo da sequência de cores.
        level (int): nível atual do jogo.
        blink_index (int): índice de piscagem da luz do botão.
        blink_counter (int): contador usado para controlar a piscagem da luz do botão.
        blink_interval (int): intervalo em que a luz do botão pisca.
        sequence_delay_counter (int): contador usado para controlar o tempo entre as sequências de cores.
        start_counter (int): contador usado para controlar o tempo de espera para iniciar o jogo.
        start_timer (int): tempo de espera para gerar uma nova sequência de cores.
        animation_counter (int): contador usado para controlar a animação inicial do jogo.
        is_animating (bool): status de animação do jogo.

    Métodos:
        set_buttons(self, buttons: ColoredButton) -> None:
            Define os botões coloridos do jogo.
        set_start_button(self, start_button: StartButton) -> None:
            Define o botão de início do jogo.
        start(self) -> None:
            Redefine o nível inicial e zera o contador.
        new_sequence(self) -> List[int]:
            Gera uma nova sequência de cores aleatórias.
        blink_buttons(self) -> None:
            Pisca as luzes dos botões de acordo com a sequência de cores.
        start_animation(self) -> None:
            Inicia a animação de início do jogo.
        check_sequence(self, button: Any) -> None:
            Verifica a sequência de cores do jogo de acordo com o botão pressionado.
        update(self) -> None:
            Atualiza o estado do jogo de acordo com o status de animação e sequência de cores.

    """

    INITIAL_LEVEL = 1
    ANIMATION_DURATION = 60

    def __init__(self):
        """
        Inicializa a classe Game.

        Returns:
            None
        """
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

    def set_buttons(self, buttons: ColoredButton) -> None:
        """
        Define os botões coloridos do jogo.

        Esta função recebe uma lista de botões coloridos e define os botões do jogo.

        Argumentos:
            buttons (ColoredButton): lista de botões coloridos.

        Retorna:
            None
        """
        self.buttons = buttons

    def set_start_button(self, start_button: StartButton) -> None:
        """
        Define o botão de início do jogo.

        Esta função recebe o botão de início do jogo e define o botão do jogo.

        Argumentos:
            start_button (StartButton): botão de início do jogo.

        Retorna:
            None
        """
        self.start_button = start_button

    def start(self) -> None:  # Redefine o nível inicial e zera o contador
        """
        Inicia o jogo.

        Esta função redefine o nível inicial do jogo e zera o contador para iniciar o jogo.

        Retorna:
            None
        """
        self.level = Game.INITIAL_LEVEL
        self.start_counter = 0  # Zera o contador toda vez que o botão é apertado, desse modo é possível resetar o jogo

    def new_sequence(self) -> List[int]:
        """
        Gera uma nova sequência de cores.

        Esta função gera uma nova sequência de cores aleatórias de acordo com o nível atual do jogo.

        Retorna:
            List[int]: lista com a sequência de cores gerada.
        """
        self.sequence = [random.randint(0, 3) for _ in range(self.level)]
        self.next_step = 0
        self.blink_index = 0
        self.blink_counter = 0

        return self.sequence

    def blink_buttons(self) -> None:
        """
        Pisca as luzes dos botões de acordo com a sequência de cores.

        Esta função controla a piscagem das luzes dos botões de acordo com a sequência de cores.

        Retorna:
            None
        """
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

    def start_animation(self) -> None:
        """
        Inicia a animação de início do jogo.

        Esta função inicia a animação de início do jogo, piscando as luzes dos botões.

        Retorna:
            None
        """
        self.is_animating = True
        self.animation_counter = 0

        for button in self.buttons:
            button.start_blink()

    def check_sequence(self, button: Any) -> None:
        """
        Verifica a sequência de cores do jogo de acordo com o botão pressionado.

        Esta função é chamada quando um botão colorido é pressionado e verifica se a sequência de cores foi seguida corretamente.

        Argumentos:
            button (Any): botão colorido pressionado.

        Retorna:
            None
        """
        expect = self.sequence[self.next_step]
        pressed_button = self.buttons.index(button)
        if pressed_button == expect:
            self.next_step += 1
            player.increase_score()
            if self.next_step == len(self.sequence):
                reinforcement_phrase = random.choice(positive_reinforcement_phrases)
                print(reinforcement_phrase)
                self.sequence_delay_counter = 0
                self.level += 1
                self.sequence_delay_counter = 1
        else:
            reinforcement_phrases = random.choice(negative_reinforcement_phrases)
            print(reinforcement_phrases)
            print(f"You got {player.score} points!")
            self.next_step = 0
            self.level = Game.INITIAL_LEVEL

    def update(self) -> None:
        """
        Atualiza o estado do jogo.

        Esta função é chamada periodicamente para atualizar o estado do jogo de acordo com o status de animação e sequência de cores.

        Retorna:
            None
        """
            
        if self.is_animating:
            if self.animation_counter < Game.ANIMATION_DURATION:
                for button in self.buttons:
                    button.update()
                self.animation_counter += 1
            else:
                for button in self.buttons:
                    button.stop_blink()

                self.is_animating = False

                if start_button.start_status:
                    self.new_sequence()

        else:
            if self.blink_index < len(self.sequence) and start_button.start_status:
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
    player = Player()
    game = Game()

    start_button = StartButton(game)
    yellow_button = ColoredButton(YELLOW_OFF, 321, 396, YELLOW_OFF)
    red_button = ColoredButton(RED_OFF, 572, 145, RED_OFF)
    blue_button = ColoredButton(BLUE_OFF, 578, 395, BLUE_OFF)
    green_button = ColoredButton(GREEN_OFF, 320, 145, GREEN_OFF)
    game.set_buttons([yellow_button, red_button, blue_button, green_button])
    game.set_start_button(start_button)

    run(globals())
