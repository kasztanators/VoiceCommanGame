import numpy as np
import pygame
from settings import *
import sys
from map import Map
from wizard import Wizard
from warrior import Warrior
import tensorflow as tf
from SpeechRecognition.code.recording_functions import record_audio
from SpeechRecognition.code.tensor_functions import preprocess_audiobuffer
class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.map = Map()
        self.wizard = Wizard()
        self.warrior = Warrior()
        self.wizard.add_enemy(self.warrior)
        self.warrior.add_enemy(self.wizard)# warrior speaks
        self.commands = ['down','go', 'left','right', 'stop', 'up', 'yes']
        self.loaded_model = tf.keras.models.load_model("C:/Users/User/PycharmProjects/VoiceCommandGame/code/saved_model/saved")
        self.push_to_talk = False
        self.push_to_talk_release = False
        self.found_command = False
        self.ptt_img = pygame.image.load("./assets/images/others/speech.png").convert_alpha()

    def run(self):
        pygame.init()

        while True:
            key = pygame.key.get_pressed()
            predicted_command = ""
            command = ""

            if key[pygame.K_SPACE]:

                self.draw_ptt()
                pygame.display.update()
                predicted_command = self.predict_mic()
                self.found_command = True

            if self.found_command:
                command = predicted_command
                self.found_command = False
                print(command)

            self.warrior.move(command)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.refresh()
            pygame.display.update()
            self.clock.tick(60)

    def refresh(self):
        self.map.refresh(self.screen)
        self.wizard.move()
        self.warrior.refresh(self.screen)
        self.wizard.refresh(self.screen)

    def predict_mic(self):
        audio = record_audio()
        spec = preprocess_audiobuffer(audio)
        prediction = self.loaded_model(spec)
        label_prediction = np.argmax(prediction, axis=1)
        command = self.commands[label_prediction[0]]
        return command
    def draw_ptt(self):
        self.screen.blit(self.ptt_img, (SCREEN_WIDTH-103, 23))
