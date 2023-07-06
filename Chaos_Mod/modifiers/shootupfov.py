import unrealsdk as unrealsdk
from unrealsdk import *

class modifier:
    def __init__(self):
        self.name = "Shoot Up FOV"
        self.description = "Makes the FOV go up when shooting"
        self.pc = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.world = unrealsdk.GetEngine().GameViewport.World

    def activate(self):
        def fov(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
            try:
                self.pc.Pawn.CameraComponent.FieldOfView = 100
            except:
                pass
            return True
        unrealsdk.RegisterHook('/Script/GbxGameSystemCore.DamageComponent.ReceiveAnyDamage', 'fov', fov)

    def deactivate(self):
        unrealsdk.RemoveHook('/Script/GbxGameSystemCore.DamageComponent.ReceiveAnyDamage', 'fov')