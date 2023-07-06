import unrealsdk as unrealsdk
from unrealsdk import *

class modifier:
    def __init__(self):
        self.name = "Toggle HUD"
        self.description = "Toggles the HUD on and off"
        self.pc = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.world = unrealsdk.GetEngine().GameViewport.World

    def activate(self):
        unrealsdk.Log("Toggling HUD")
        hud = self.pc.GetHUD()
        hud.SetHUDVisible(self.pc, False)

    def deactivate(self):
        hud = self.pc.GetHUD()
        hud.SetHUDVisible(self.pc, True)