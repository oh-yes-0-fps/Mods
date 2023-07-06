import unrealsdk as unrealsdk
from unrealsdk import *



class modifier:
    def __init__(self):
        self.name = "Butter Fingers"
        self.description = "All Entities Drops Item On Taking Damage"
        self.pc = unrealsdk.GetEngine().GameInstance.LocalPlayers[0].PlayerController
        self.world = unrealsdk.GetEngine().GameViewport.World

    def activate(self):
        def dropitem(caller: unrealsdk.UObject, function: unrealsdk.UFunction, params: unrealsdk.FStruct) -> bool:
            try:
                caller.GetOwner().DropCurrentWeapon()
            except:
                pass
            return True
        unrealsdk.RegisterHook('/Script/GbxGameSystemCore.DamageComponent.ReceiveAnyDamage', 'butter_dropitem', dropitem)

    def deactivate(self):
        unrealsdk.RemoveHook('/Script/GbxGameSystemCore.DamageComponent.ReceiveAnyDamage', 'butter_dropitem')