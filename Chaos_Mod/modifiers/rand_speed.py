import unrealsdk as unrealsdk
from unrealsdk import *
import random

class modifier:
    def __init__(self):
        self.name = "Random Speed"
        self.description = "Randomizes the speed of the player"
        self.pc = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.world = unrealsdk.GetEngine().GameViewport.World

    def activate(self):
        ground_speed = self.pc.Pawn.OakCharacterMovement.MaxGroundSpeedScale
        set_speed = float(random.randint(1, 100) / 10)
        while set_speed > 0.7 and set_speed < 2.8:
            set_speed = float(random.randint(1, 100) / 10)
        ground_speed.Value = set_speed
        ground_speed.BaseValue = set_speed

    def deactivate(self):
        ground_speed = self.pc.Pawn.OakCharacterMovement.MaxGroundSpeedScale
        ground_speed.Value = 1.0
        ground_speed.BaseValue = 1.0
