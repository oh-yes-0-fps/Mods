import unrealsdk as unrealsdk
from unrealsdk import *


class modifier:
    def __init__(self):
        self.name = "The Floor is Ice"
        self.description = "Turns the floor to ice"
        self.pc = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.world = unrealsdk.GetEngine().GameViewport.World

    def activate(self):
        self.pc.Pawn.OakCharacterMovement.GroundFriction = 0.0
        self.pc.Pawn.OakCharacterMovement.BrakingDecelerationWalking = 0.0
        self.pc.Pawn.OakCharacterMovement.MaxAcceleration = 333

    def deactivate(self):
        self.pc.Pawn.OakCharacterMovement.MaxAcceleration = 2048
        self.pc.Pawn.OakCharacterMovement.GroundFriction = 15.0
        self.pc.Pawn.OakCharacterMovement.BrakingDecelerationWalking = 1900.0
