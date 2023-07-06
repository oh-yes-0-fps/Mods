import unrealsdk as unrealsdk
from unrealsdk import *




class modifier:
    def __init__(self):
        self.name = "Lower Gravity"
        self.description = "Lowers the gravity"
        self.pc = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.world = unrealsdk.GetEngine().GameViewport.World

    def activate(self):
        self.pc.Pawn.OakCharacterMovement.GravityScale = 0.1

    def deactivate(self):
        self.pc.Pawn.OakCharacterMovement.GravityScale = 1.0